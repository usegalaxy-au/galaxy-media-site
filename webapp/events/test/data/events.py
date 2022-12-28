"""Data for test setup."""

from .locations import TEST_LOCATIONS
from .supporters import TEST_SUPPORTERS
from .tags import TEST_TAGS

TEST_EVENTS = [
    {
        "data": {
            "title": "Test Event 1",
            "body": "# Test event body\n\nThe event body in markdown.",
            "is_published": True,
        },
        "relations": {
            "locations": [TEST_LOCATIONS[0]],
            "supporters": [TEST_SUPPORTERS[0]],
            "tags": [TEST_TAGS[0]],
        },
    },
    {
        "data": {
            "title": "Test Event 2",
            "body": "# Test event body\n\nThis event has not been published.",
        },
        "relations": {
            "locations": [TEST_LOCATIONS[0]],
            "supporters": [TEST_SUPPORTERS[0]],
            "tags": [TEST_TAGS[0]],
        },
    },
    {
        "data": {
            "title": "Test Event 3 - external event",
            "external": "https://example.com",
            "is_published": True,
        },
        "relations": {
            "locations": [TEST_LOCATIONS[0]],
            "supporters": [TEST_SUPPORTERS[0], TEST_SUPPORTERS[1]],
            "tags": [TEST_TAGS[0], TEST_TAGS[1]],
        },
    },
]
