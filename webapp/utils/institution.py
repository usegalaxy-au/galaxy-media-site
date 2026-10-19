"""Validate against institutions.

Institutions and their approved email domains are fetched from the Galaxy
Australia infrastructure repository and cached locally.
"""

import json
import logging
import os
import re
import tempfile
import time
from pathlib import Path

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

APPROVED_DOMAINS_URL = (
    'https://raw.githubusercontent.com/usegalaxy-au/infrastructure/'
    'refs/heads/master/roles/grouper/files/approved_domains.json')
CACHE_SECONDS = 86400  # 24 hours
RETRY_COOLDOWN_SECONDS = 3600  # 1 hour - wait after a failed refresh
REQUEST_TIMEOUT_SECONDS = 10
CACHE_DIR = Path(settings.MEDIA_ROOT) / 'institutions'
INSTITUTIONS_CACHE_PATH = CACHE_DIR / 'institutions.json'
DOMAINS_CACHE_PATH = CACHE_DIR / 'domains.json'


def is_institution_email(email):
    """Return True if given address is for valid institution.

    Match against exact domain and also root domains.
    e.g. if 'uq.edu.au' is a listed domain, then 'blah.uq.edu.au' will also
    return True.
    """
    if not _is_valid_email(email):
        raise ValueError(f"'{email}' is not a valid email address")
    domain = email.split('@')[1]
    # For me@abc.xyz.edu.au, check also root domains xyz.edu.au, edu.au
    possible_root_domains = {
        '@' + '.'.join(domain.split('.')[i:])
        for i in range(len(domain.split('.')) - 1)
    }

    # Hard-check against all email domains
    valid_domains = [
        d.replace('*.', '@')  # All matched against root domains anyway
        for d in get_email_domains()
    ]
    matching_domains = set(valid_domains) & possible_root_domains
    if matching_domains:
        return True

    # Check against wildcard domains
    wildcard_domain_matches = [
        d.replace('*', '.')
        for d in valid_domains
        if '*' in d
        and re.match(d.replace('*', '.+'), domain)
    ]
    if wildcard_domain_matches:
        return True
    return False


def get_institutions():
    """Return list of institutions sorted by name.

    Each institution is a dict with keys 'name' and 'domains', where domains
    are bare (e.g. 'uq.edu.au') or wildcard (e.g. '*.gov.au').
    """
    return _read_cache(INSTITUTIONS_CACHE_PATH)


def get_email_domains():
    """Return dictionary of email domains mapped to institution names.

    Domains are prefixed with '@' (e.g. '@uq.edu.au') unless wildcard
    (e.g. '*.gov.au').
    """
    return _read_cache(DOMAINS_CACHE_PATH)


def _is_valid_email(email):
    """Return True if given address is valid."""
    return re.match(r'^[^@]+@[^@]+\.[^@]+$', email)


def _read_cache(path):
    """Read JSON from cache file, refreshing from remote if expired."""
    if not _is_cache_fresh(path):
        try:
            _refresh_cache()
        except (
            requests.RequestException,
            ValueError,
            KeyError,
            OSError,
        ) as exc:
            if not path.exists():
                raise
            logger.warning(
                f"Failed to fetch approved domains from"
                f" {APPROVED_DOMAINS_URL} - using stale cache: {exc}")
            _defer_refresh()
    with open(path) as f:
        return json.load(f)


def _is_cache_fresh(path):
    """Return True if cache file exists and is within cache expiry time."""
    return (
        path.exists()
        and os.path.getmtime(path) > time.time() - CACHE_SECONDS
    )


def _defer_refresh():
    """Mark stale cache as fresh until the retry cooldown expires.

    Prevents every request blocking on a slow/unreachable remote.
    """
    mtime = time.time() - CACHE_SECONDS + RETRY_COOLDOWN_SECONDS
    for path in (INSTITUTIONS_CACHE_PATH, DOMAINS_CACHE_PATH):
        if path.exists():
            os.utime(path, (mtime, mtime))


def _refresh_cache():
    """Fetch approved domains from remote and write both cache files."""
    response = requests.get(
        APPROVED_DOMAINS_URL,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    institutions = _build_institutions(response.json())
    domains = _build_domains(institutions)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    _write_json_atomic(INSTITUTIONS_CACHE_PATH, institutions)
    _write_json_atomic(DOMAINS_CACHE_PATH, domains)


def _write_json_atomic(path, data):
    """Write JSON to a temp file and move into place.

    Prevents concurrent workers/threads from reading a partially written
    file. Each call writes to its own unique temp file.
    """
    fd, tmp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=path.name,
        suffix='.tmp',
    )
    try:
        with os.fdopen(fd, 'w') as f:
            json.dump(data, f, indent=2)
        os.replace(tmp_path, path)
    except BaseException:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise


def _build_institutions(data):
    """Return sorted list of institutions from remote approved domains."""
    institutions = [
        {
            'name': group['name'],
            'domains': sorted(
                (domain.strip().lower() for domain in group['domains']),
                key=lambda d: not d.startswith('*'),  # Wildcards first
            ),
        }
        for group in data.values()
    ]
    return sorted(institutions, key=lambda i: i['name'].lower())


def _build_domains(institutions):
    """Return dictionary of email domains mapped to institution names."""
    return {
        _normalise_domain(domain): institution['name']
        for institution in institutions
        for domain in institution['domains']
    }


def _normalise_domain(domain):
    """Prefix bare domain with '@' for email matching."""
    domain = domain.strip().lower()
    if domain.startswith(('@', '*')):
        return domain
    return '@' + domain
