"""Settings for production."""

import os
import sentry_sdk

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

# To allow cross-site resource sharing with the base domain
CSRF_COOKIE_DOMAIN = os.getenv("CSRF_COOKIE_DOMAIN", ".usegalaxy.org.au")
CSRF_TRUSTED_ORIGINS = [
    "http://*.usegalaxy.org.au",
    "https://*.usegalaxy.org.au",
    "http://*.gvl.org.au",
    "https://*.gvl.org.au",
    f"http://{HOSTNAME}",
    f"https://{HOSTNAME}",
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
STATICFILES_STORAGE = (
    'django.contrib.staticfiles.storage'
    '.ManifestStaticFilesStorage')

sentry_sdk.init(
    dsn="https://426e64399bbafe4210c4fa647c7a2f5b@sentry.galaxyproject.org/20",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
)
