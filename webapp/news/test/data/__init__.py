from .news import TEST_NEWS, BIOCOMMONS_HTML, HUB_JSON
from ...scrape import biocommons, hub

MOCK_REQUESTS = {
    biocommons.URL: BIOCOMMONS_HTML,
    hub.URL: HUB_JSON,
}
