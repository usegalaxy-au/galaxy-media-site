"""Development settings."""

import os

from .base import *
from .log import config
from utils.parse import parse_list


DEBUG = True
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY') or "secretkey"
if os.environ.get('HOSTNAME'):
    HOSTNAME = os.environ.get('HOSTNAME')
    ALLOWED_HOSTS.append(HOSTNAME)

# Rendered as "Galaxy <GALAXY_SITE_NAME> <GALAXY_SITE_SUFFIX>"
GALAXY_SITE_NAME = 'Australia'
GALAXY_SITE_SUFFIX = 'Media'

# For posting tool update notifications to a Slack channel
SLACK_API_URLS = parse_list(os.environ.get('SLACK_API_URLS'))
TOOL_UPDATE_EMAILS = parse_list(os.environ.get('TOOL_UPDATE_EMAILS'))

# Validating whether submitted email is valid Galaxy AU account
MOCK_GALAXY_EMAIL_VALIDATION = True

SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']

INTERNAL_IPS = [
    "127.0.0.1",
]

INSTALLED_APPS.append('debug_toolbar')
MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3'
    }
}

LOGGING = config.configure_logging(LOG_ROOT)
