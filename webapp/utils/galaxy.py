"""Connect with Galaxy server."""

import time
import logging
from bioblend.galaxy import GalaxyInstance
from django.conf import settings

logger = logging.getLogger('django')


def is_registered_galaxy_email(email):
    """Return True if a Galaxy account exists on the given server."""
    if not (settings.GALAXY_URL and settings.GALAXY_API_KEY):
        logging.error("Trying to access Galaxy with no credentials set!")
        return False
    gi = GalaxyInstance(settings.GALAXY_URL, key=settings.GALAXY_API_KEY)
    t0 = time.time()
    users = gi.users.get_users()  # Cache this?
    td = round((time.time() - t0) * 1000)
    logger.info(f"Galaxy user email list requested in {td} ms")
    return email in [u['email'] for u in users]
