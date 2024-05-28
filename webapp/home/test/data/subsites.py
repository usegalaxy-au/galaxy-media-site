"""Data for test setup.

TODO: this needs to be updated for new exported lab pages.
"""

import os
from pathlib import Path

CONTENT_DIR = (
    Path(__file__).parent.parent.parent
    / 'static/home/labs/docs'
)
MOCK_BASE_URL = 'http://mockserver/static/home/labs/genome'


# Collect all the files from the lab's content dir and assign each
# file's content to a URL in the mock server.
MOCK_REQUESTS = {}
for root, dirs, files in os.walk(CONTENT_DIR):
    for file in files:
        with open(os.path.join(root, file)) as f:
            relpath = root.replace(str(CONTENT_DIR), '') + '/' + file
            relpath = relpath.lstrip('/')
            MOCK_REQUESTS[f'{MOCK_BASE_URL}/{relpath}'] = f.read()

TEST_SUBSITES = [
    {
        "name": "main",
    },
    {
        "name": "genome",
    },
]
