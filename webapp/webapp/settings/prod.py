"""Settings for production."""

import os

from .base import *
from . import validate
from .log import config
from utils.parse import parse_list

validate.env()

DEBUG = False
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
HOSTNAME = os.environ['HOSTNAME']

ALLOWED_HOSTS.append(HOSTNAME)
ALLOWED_HOSTS.append("usegalaxy.org.au")
ALLOWED_HOSTS.append("dev.usegalaxy.org.au")
ALLOWED_HOSTS.append("staging.usegalaxy.org.au")
MOCK_GALAXY_INTERACTIONS = 'MOCK_GALAXY_INTERACTIONS' in os.environ

# To allow cross-site resource sharing with the base domain
CSRF_COOKIE_DOMAIN = ".usegalaxy.org.au"
CSRF_TRUSTED_ORIGINS = [
    "https://*.usegalaxy.org.au"
]

# Rendered as "Galaxy <GALAXY_SITE_NAME> <GALAXY_SITE_SUFFIX>"
GALAXY_SITE_NAME = 'Australia'
GALAXY_SITE_SUFFIX = 'Media'

# For posting tool update notifications to Slack
SLACK_API_URLS = parse_list(os.environ.get('SLACK_API_URLS'))
TOOL_UPDATE_EMAILS = parse_list(os.environ.get('TOOL_UPDATE_EMAILS'))

RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_SITE_KEY')
RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_SECRET_KEY')

# See base.py for mail config, read from .env

ADMINS = [
    ('Cameron', 'c.hyde@qcif.edu.au'),
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

LOGGING = config.configure_logging(LOG_ROOT)

# Use manifest to manage static file versions for cache busting:
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
