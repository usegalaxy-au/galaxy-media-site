"""Development settings."""

import os
from pathlib import Path

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

SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

LOGGING = config.configure_logging(LOG_ROOT)

MEDIA_ROOT = Path('/tmp/gms-media')
