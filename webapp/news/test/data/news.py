"""Data for test setup."""

from pathlib import Path
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

with open(Path(__file__).parent / 'biocommons.html') as f:
    BIOCOMMONS_HTML = f.read()

HUB_JSON = {
  "count": 3,
  "news": [
    {
      "id": "0e840460",
      "title": "Carbon Emissions Reporting in Galaxy",
      "tease": "Dynamic carbon emissions reporting for jobs in Galaxy",
      "days_ago": 9,
      "date": "11 July 2023",
      "subsites": [
        "global",
        "freiburg",
        "pasteur",
        "belgium",
        "ifb",
        "genouest",
        "erasmusmc",
        "elixir-it",
        "au",
        "eu",
        "us"
      ],
      "main_subsite": None,
      "tags": [
        "UI/UX",
        "highlight"
      ],
      "contact": "",
      "image": None,
      "authors": "Rendani Gangazhe",
      "authors_structured": [
        {
          "github": "Renni771"
        }
      ],
      "external_url": "",
      "path": "/news/2023-07-11-carbon-emissions-reporting/"
    },
    {
      "id": "567281e4",
      "title": "Platform for Advanced Scientific Computing Conference 2023",
      "tease": "Several Galaxy Community members gathered in Davos",
      "days_ago": 13,
      "date": "7 July 2023",
      "subsites": [
        "global",
        "freiburg",
        "pasteur",
        "belgium",
        "ifb",
        "genouest",
        "erasmusmc",
        "elixir-it",
        "eu"
      ],
      "main_subsite": None,
      "tags": [],
      "contact": "",
      "image": None,
      "authors": "Hans-Rudolf Hotz",
      "authors_structured": [],
      "external_url": "",
      "path": "/news/2023-07-07-pasc-conference/"
    },
    {
      "id": "75894ca7",
      "title": "Galaxy Single-cell Updates",
      "tease": "Latest updates on Galaxy tools, workflows and training materials developed by the Galaxy single-cell community",
      "days_ago": 20,
      "date": "30 June 2023",
      "subsites": [
        "eu",
        "freiburg",
        "pasteur",
        "belgium",
        "ifb",
        "genouest",
        "erasmusmc",
        "elixir-it",
        "au",
        "us",
        "global"
      ],
      "main_subsite": "eu",
      "tags": [],
      "contact": "",
      "image": None,
      "authors": "",
      "authors_structured": [],
      "external_url": "",
      "path": "/news/2023-06-30-single-cell-updates/"
    },
  ]
}
