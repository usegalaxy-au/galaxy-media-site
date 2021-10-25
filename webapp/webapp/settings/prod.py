"""Settings for production."""

from dotenv import load_dotenv

from .base import *


load_dotenv()

DEBUG = False
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
ALLOWED_HOSTS.append('site.usegalaxy.org')

# DATABASES = {
#     # Probably want a proper production database e.g. postgres
# }
