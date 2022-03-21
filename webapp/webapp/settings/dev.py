"""Development settings."""

import os

from .base import *
from .log import config

DEBUG = False
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY') or "secretkey"
if os.environ.get('HOSTNAME'):
    HOSTNAME = os.environ.get('HOSTNAME')
    ALLOWED_HOSTS.append(HOSTNAME)

# Rendered as "Galaxy <GALAXY_SITE_NAME> <GALAXY_SITE_SUFFIX>"
GALAXY_SITE_NAME = 'Australia'
GALAXY_SITE_SUFFIX = 'Media'

# For posting tool update notifications to a Slack channel
SLACK_API_URL = os.environ.get('SLACK_API_URL')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "secretkey"

SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ga_site',
        'USER': 'cameron',
        'PASSWORD': 'secret',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

LOGGING = config.configure_logging(LOG_ROOT)
