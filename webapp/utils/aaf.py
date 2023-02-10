"""Functions for fetching and parsing AAF institutions list."""

import os
import time
import requests
from bs4 import BeautifulSoup

from django.conf import settings

CACHE_SECONDS = 259200  # 72 hours
METADATA_URL = "https://md.aaf.edu.au/aaf-metadata.xml"
METADATA_PATH = os.path.join(settings.MEDIA_ROOT, 'aaf.xml')


def fetch_metadata():
    """Fetch the file from the cache or remote."""
    if os.path.exists(METADATA_PATH):
        if os.path.getmtime(METADATA_PATH) > time.time() - CACHE_SECONDS:
            # Local file within cache expiry time
            with open(METADATA_PATH) as f:
                return f.read()
    r = requests.get(METADATA_URL)
    content = r.content.decode('utf-8')
    with open(METADATA_PATH, 'w') as f:
        f.write(content)
    return content


def get_entities():
    """Return a list of domain names under AAF registration."""
    content = fetch_metadata()
    soup = BeautifulSoup(content, 'xml')
    entities = []
    for el in soup.find_all('EntityDescriptor'):
        title = el.find("OrganizationDisplayName").text
        if title.lower() == "australian access federation":
            continue
        if title not in entities:
            entities.append(title)
    return sorted(entities)
