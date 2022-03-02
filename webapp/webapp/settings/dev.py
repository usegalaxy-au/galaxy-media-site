"""Development settings."""

import os
from dotenv import load_dotenv

from .base import *

load_dotenv('../.env', override=True)

DEBUG = False
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY') or "secretkey"
GALAXY_SITE_NAME = 'Australia'  # Rendered as "Galaxy <GALAXY_SITE_NAME> Media"
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

# Galaxy AU mail server
# EMAIL_HOST = os.environ['MAIL_HOSTNAME']
# EMAIL_PORT = os.environ['MAIL_SMTP_PORT']
# EMAIL_HOST_USER = os.environ['MAIL_SMTP_USERNAME']
# EMAIL_HOST_PASSWORD = os.environ['MAIL_SMTP_PASSWORD']
# EMAIL_HOST_USE_TLS = os.environ.get('MAIL_USE_TLS') or False
EMAIL_FROM_ADDRESS = os.environ['MAIL_TO_ADDRESS']
EMAIL_TO_ADDRESS = os.environ['MAIL_TO_ADDRESS']
