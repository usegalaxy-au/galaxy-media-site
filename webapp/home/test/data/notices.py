"""Data for test setup."""

from .subsites import TEST_LABS

TEST_NOTICES = [
    {
        "data": {
            "notice_class": "info",
            "title": "Test Notice 1",
            "short_description": "Test Notice 1",
            "body": "# Test notice body\n\nThe notice body in markdown.",
            "enabled": True,
            "is_published": True,
        },
        "relations": {
            "subsites": [TEST_LABS[0]],
        },
    },
    {
        "data": {
            "notice_class": "info",
            "title": "Test Notice 2",
            "short_description": "Test Notice 2",
            "body": (
                "# Test notice body 2\n\n"
                "Another arbitrary info notice."
                " This one will also be displayed on a second subsite."
            ),
            "enabled": True,
            "is_published": True,
        },
        "relations": {
            "subsites": [TEST_LABS[0]],
        },
    },
    {
        "data": {
            "notice_class": "info",
            "title": "Test Notice 3",
            "short_description": "Test Notice 3",
            "body": (
                "# Test notice body 3\n\nThis notice is not yet published."
            ),
            "enabled": True,
        },
        "relations": {
            "subsites": [TEST_LABS[0]],
        },
    },
    {
        "data": {
            "notice_class": "warning",
            "title": "Test Notice 4",
            "short_description": "Test Notice 4 - a block notice",
            "body": (
                "# A warning notice 3\n\nThis is a warning message."
            ),
            "enabled": True,
            "is_published": True,
            "static_display": True,
        },
        "relations": {
            "subsites": [TEST_LABS[0]],
        },
    },
]
