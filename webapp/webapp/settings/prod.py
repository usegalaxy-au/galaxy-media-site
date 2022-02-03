"""Settings for production."""

import os
from dotenv import load_dotenv

from .base import *


load_dotenv('../.env', override=True)

DEBUG = False
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
HOSTNAME = os.environ['HOSTNAME']
ALLOWED_HOSTS.append(HOSTNAME)
GALAXY_SITE_NAME = 'Media'  # Rendered as "Galaxy <GALAXY_SITE_NAME>"

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

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ['MAIL_HOSTNAME']
EMAIL_PORT = os.environ['MAIL_SMTP_PORT']
EMAIL_HOST_USER = os.environ['MAIL_SMTP_USERNAME']
EMAIL_HOST_PASSWORD = os.environ['MAIL_SMTP_PASSWORD']
EMAIL_HOST_USE_TLS = os.environ.get('MAIL_USE_TLS', False)
