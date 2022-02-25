"""Settings for production."""

import os
from dotenv import load_dotenv

from .base import *
from . import validate


load_dotenv('../.env', override=True)
validate.env()

DEBUG = False
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
HOSTNAME = os.environ['HOSTNAME']

ALLOWED_HOSTS.append(HOSTNAME)
GALAXY_SITE_NAME = 'Australia'  # Rendered as "Galaxy <GALAXY_SITE_NAME> Media"

# For posting tool update notifications to Slack
SLACK_API_URL = (
    "https://hooks.slack.com/services"
    "/T01BG9M9LFJ/B034ECV1Y8Z/8BcMUWPZE3LCDcxJXkqmT4b6"
)

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
