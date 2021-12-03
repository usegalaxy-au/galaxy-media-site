"""Development settings."""

import os
from dotenv import load_dotenv

from .base import *


load_dotenv()

DEBUG = False
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY') or "secretkey"
HOSTNAME = os.environ['HOSTNAME']
ALLOWED_HOSTS.append(HOSTNAME)
GALAXY_SITE_NAME = 'Media'  # Rendered as "Galaxy <GALAXY_SITE_NAME>"

DEBUG = True

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
