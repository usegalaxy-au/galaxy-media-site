"""Development settings."""

import os
from dotenv import load_dotenv

from .base import *

load_dotenv('../.env', override=True)

DEBUG = False
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY') or "secretkey"
GALAXY_SITE_NAME = 'Media'  # Rendered as "Galaxy <GALAXY_SITE_NAME>"
if os.environ.get('HOSTNAME'):
    HOSTNAME = os.environ.get('HOSTNAME')
    ALLOWED_HOSTS.append(HOSTNAME)

# For posting tool update notifications to Slack
SLACK_API_URL = (
    "https://hooks.slack.com/services"
    "/T01BG9M9LFJ/B034ECV1Y8Z/8BcMUWPZE3LCDcxJXkqmT4b6"
)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "secretkey"

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
