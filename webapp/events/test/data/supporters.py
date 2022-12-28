"""Data for test setup."""

from django.conf import settings

SUPPORTER_FILE_PREFIX = '~test-supporter'

TEST_SUPPORTERS = [
    {
        "data": {
            "name": "Supporter A",
            "url": "https://supporter-a-website.com",
        },
        "files": {
            "logo": (
                settings.BASE_DIR
                / f"events/test/data/media/supporter-a-logo.png"
            ),
        },
    },
    {
        "data": {
            "name": "Supporter B",
            "url": "https://supporter-b-website.com",
        },
        "files": {
            "logo": (
                settings.BASE_DIR
                / f"events/test/data/media/supporter-b-logo.png"
            ),
        },
    },
]
