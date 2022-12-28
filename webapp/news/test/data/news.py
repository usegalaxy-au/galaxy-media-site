"""Data for test setup."""

from events.test.data import TEST_SUPPORTERS, TEST_TAGS

TEST_NEWS = [
    {
        "data": {
            "title": "Test News 1",
            "body": "# Test news body\n\nThe news body in markdown.",
            "is_published": True,
        },
        "relations": {
            "tags": [
                TEST_TAGS[0],
            ],
            "supporters": [
                TEST_SUPPORTERS[0],
            ],
        },
    },
    {
        "data": {
            "title": "Test News 2",
            "body": (
                "# Test news body\n\n"
                "Another news article in markdown."
                " This one is unpublished."
            ),
            "is_published": False,
        },
        "relations": {
            "tags": [
                TEST_TAGS[0],
            ],
            "supporters": [
                TEST_SUPPORTERS[0],
            ],
        },
    },
    {
        "data": {
            "title": "Test News 3",
            "body": (
"""---
site: freiburg
title: 'Galaxy Australia tool updates 2022-12-14'
tags: [tools]
supporters:
    - galaxyaustralia
    - melbinfo
    - qcif
---

### Tools installed

| Section | Tool |
|---------|-----|
| **Convert Formats** | vcf2maf [e8510e04a86a](https://toolshed.g2.bx.psu.edu/view/iuc/vcf2maf/e8510e04a86a) |
"""
            ),
            "is_published": True,
            "is_tool_update": True,
        },
        "relations": {
            "tags": [
                TEST_TAGS[1],
            ],
            "supporters": [
                TEST_SUPPORTERS[0],
                TEST_SUPPORTERS[1],
            ],
        },
    },
]
