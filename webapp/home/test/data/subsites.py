"""Data for test setup.

TODO: this needs to be updated for new exported lab pages.
"""

from pathlib import Path

MEDIA_DIR = Path(__file__).parent.parent.parent / 'labs/docs'
MOCK_BASE_URL = 'http://mockserver'
MOCK_REQUESTS = {}
# for file in MEDIA_DIR.iterdir():
#     with open(file) as f:
#         MOCK_REQUESTS[f'{MOCK_BASE_URL}/{file.name}'] = f.read()

TEST_SUBSITES = [
    {
        "name": "main",
    },
    {
        "name": "genome",
    },
]
