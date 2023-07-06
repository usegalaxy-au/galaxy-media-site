"""Connect with Galaxy server."""

import logging
from bioblend.galaxy import GalaxyInstance
from django.conf import settings

logger = logging.getLogger('django')


def get_galaxy_instance():
    """Return a GalaxyInstance object or None if failed."""
    if not (settings.GALAXY_URL and settings.GALAXY_API_KEY):
        logging.error("Trying to access Galaxy with no credentials set!")
        return None
    return GalaxyInstance(settings.GALAXY_URL, key=settings.GALAXY_API_KEY)


def is_registered_email(email):
    """Return True if a Galaxy account exists on the given server."""
    if settings.MOCK_GALAXY_EMAIL_VALIDATION:
        return True

    if not (settings.GALAXY_URL and settings.GALAXY_API_KEY):
        logging.error("Trying to access Galaxy with no credentials set!")
        return False

    gi = get_galaxy_instance()
    if not gi:
        return False
    users = gi.users.get_users()  # Cache this?
    return email in [u['email'] for u in users]


def add_user_to_group(email, group):
    """Add a Galaxy user to the given group."""

    # TODO: remove
    raise ValueError("A fake error has occurred.")

    gi = get_galaxy_instance()
    if not gi:
        return
    users = gi.users.get_users(f_email=email)
    if not len(users):
        raise ValueError(
            f"Could not find user with email '{email}' in Galaxy AU")
    elif len(users) > 1:
        logger.error(
            f"Found multiple users with email '{email}' in Galaxy AU")
    user_id = users[0]['id']
    groups = [
        g for g in gi.groups.get_groups()
        if g['name'].lower() == group.lower()
    ]
    if not len(groups):
        raise ValueError(
            f"Could not find group with name '{group}' in Galaxy AU")
    elif len(groups) > 1:
        logger.error(
            f"Found multiple groups with name '{group}' in Galaxy AU")
    group_id = groups[0]['id']
    gi.groups.add_group_user(group_id, user_id)
