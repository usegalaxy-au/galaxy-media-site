"""Web scrapers for new sources."""

from . import biocommons, hub

# These scrapers will be called with the "scrape_news" management command.
SCRAPERS = [
    biocommons,
    hub,
]
