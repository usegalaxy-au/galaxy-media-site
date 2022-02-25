"""Add variables to global template context."""

from django.conf import settings as webapp_settings


def settings(request):
    """Include some settings variables."""
    return {'GALAXY_SITE_NAME': webapp_settings.GALAXY_SITE_NAME}
