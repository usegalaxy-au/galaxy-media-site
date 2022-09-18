"""Validate against institutions."""

import os
import json
from django.conf import settings

DOMAIN_LIST_PATH = os.path.join(
    settings.BASE_DIR,
    'utils/data/domains.json',
)
INSTITUTION_LIST_PATH = os.path.join(
    settings.BASE_DIR,
    'utils/data/institutions.json',
)


def is_institution_email(email):
    """Return True if given address is for valid institution."""
    valid_emails = get_domains()
    domain = '@' + email.split('@')[1]
    return domain in valid_emails


def get_domains():
    """Return dictionary of domains mapped to institution names."""
    with open(DOMAIN_LIST_PATH) as f:
        return json.load(f)


def get_institution_list():
    """Return list of institutions with name and email domains."""
    with open(INSTITUTION_LIST_PATH) as f:
        return json.load(f)
