"""Development settings."""

from .base import *

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
