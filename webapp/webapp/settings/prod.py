"""Settings for production."""

import os
from dotenv import load_dotenv

from .base import *


load_dotenv()

DEBUG = False
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
ALLOWED_HOSTS.append('usegalaxy-au.neoformit.com')

# DATABASES = {
#     # Probably want a proper production database e.g. postgres
# }
