"""Settings for production."""

import os
from dotenv import load_dotenv

from .base import *


load_dotenv()

DEBUG = False
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
ALLOWED_HOSTS.append('usegalaxy-au.neoformit.com')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ga_site',
        # 'USER': 'ga_site',
        # 'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
