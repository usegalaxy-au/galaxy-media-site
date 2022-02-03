"""Development settings."""

import os
from dotenv import load_dotenv

from .base import *


load_dotenv('../.env', override=True)

DEBUG = False
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY') or "secretkey"
HOSTNAME = os.environ['HOSTNAME']
ALLOWED_HOSTS.append(HOSTNAME)
GALAXY_SITE_NAME = 'Media'  # Rendered as "Galaxy <GALAXY_SITE_NAME>"

DEBUG = True

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
EMAIL_HOST = os.environ['MAIL_HOSTNAME']
EMAIL_PORT = os.environ['MAIL_SMTP_PORT']
EMAIL_HOST_USER = os.environ['MAIL_SMTP_USERNAME']
EMAIL_HOST_PASSWORD = os.environ['MAIL_SMTP_PASSWORD']
EMAIL_HOST_USE_TLS = os.environ.get('MAIL_USE_TLS') or False
