"""Context for rendering list-of-institutions.html"""

import json
from django.conf import settings

JSON = settings.BASE_DIR / 'utils/data/institutions.json'


def build_context():
    """Return context for rendering list of institutions."""
    with open(JSON) as file:
        institutions = json.load(file)
    return {'institutions': institutions}
