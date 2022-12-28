"""Data for test setup."""

from django.conf import settings

TEST_LOGO_PATH = (
    settings.BASE_DIR / "events/test/data/media/supporter-a-logo.png"
)

TEST_SUPPORTERS = [
    {
        "data": {
            "name": "Supporter A",
            "url": "https://supporter-a-website.com",
        },
        "files": {
            "logo": TEST_LOGO_PATH,
        },
    },
    {
        "data": {
            "name": "Supporter B",
            "url": "https://supporter-b-website.com",
        },
        "files": {
            "logo": TEST_LOGO_PATH,
        },
    },
]
