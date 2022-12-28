"""Custom test components for GMS."""

import os
import shutil
from django.conf import settings
from django.test import TestCase as DjangoTestCase


class TestCase(DjangoTestCase):

    def tearDown(self) -> None:
        settings_module = os.environ.get('DJANGO_SETTINGS_MODULE')
        if settings_module == 'webapp.settings.test':
            shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        else:
            raise RuntimeError(
                'Do not run tests without using webapp.settings.test!'
                f' (Using {settings_module})')
