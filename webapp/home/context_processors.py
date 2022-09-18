"""Add variables to global template context."""

from django.conf import settings as webapp_settings


def settings(request):
    """Include some settings variables."""
    return {
        'title': None,  # prevent variable not found templating error
        'HOSTNAME': webapp_settings.HOSTNAME,
        'GALAXY_SITE_NAME': webapp_settings.GALAXY_SITE_NAME,
        'GALAXY_SITE_SUFFIX': webapp_settings.GALAXY_SITE_SUFFIX,
    }
