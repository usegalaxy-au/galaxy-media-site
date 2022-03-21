"""Add variables to global template context."""

from django.conf import settings as webapp_settings


def settings(request):
    """Include some settings variables."""
    return {
        'title': None,  # prevent variable not found templating error
        'GALAXY_SITE_NAME': webapp_settings.HOSTNAME,
    }
