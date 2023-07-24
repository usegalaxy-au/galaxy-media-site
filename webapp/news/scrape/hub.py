"""Scrape news items from the Galaxy hub's cross-posted news feed.

News items from the hub can be requested from a JSON feed which returns all
news items published in the last 30 days. Items are tagged with a 'subsites'
field which lists Galaxy servers for which the content is relevant and should
be consumed.

response_schema = {
    "id": "4d078ad4",
    "title": "Carbon Emissions Reporting in Galaxy",
    "tease": "Dynamic carbon emissions reporting for jobs in Galaxy",
    "days_ago": 7,
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
            "github": "Renni771",
        },
    ],
    "external_url": "",
    "path": "/news/2023-07-11-carbon-emissions-reporting/",
}
"""

import logging
import requests
import traceback
from datetime import datetime
from news.models import News
from django.utils import timezone

logger = logging.getLogger('django')
BASE_URL = 'https://galaxyproject.org'
URL = f'{BASE_URL}/news/feed.json'


class Article:
    """An article record parsed from JSON feed content."""

    def __init__(self, data):
        """Create news item from web content."""
        self.url = BASE_URL + data['path']
        self.title = data['title']
        self.date = timezone.make_aware(datetime.strptime(
            data['date'],
            '%d %B %Y',
        ))
        self.subsites = data['subsites']

    def __str__(self):
        """Return string representation."""
        return f"Article {self.date.strftime('%Y-%m-%d')}: {self.title}"

    @classmethod
    def fetch_all(cls):
        """Fetch and parse all current news items."""
        data = cls.fetch_news_feed()
        articles = []
        for news_data in data['news']:
            try:
                articles.append(cls(news_data))
            except Exception:
                logger.error("Error parsing Galaxy Hub news article")
                logger.error(traceback.format_exc())
                logger.error("JSON response:")
                logger.error(str(data))

        return articles

    @classmethod
    def fetch_news_feed(cls):
        """Fetch news feed and parse all current news items."""
        response = requests.get(URL)
        response.raise_for_status()
        return response.json()


def fetch_articles():
    """Fetch articles and add new ones to the database."""
    articles = []
    for a in Article.fetch_all():
        if not set(a.subsites) & {'au', 'global'}:
            # This news item is not relevant to AU
            continue
        if News.objects.filter(external=a.url).count():
            # This news item already exists
            continue
        item = News.objects.create(
            title=a.title,
            external=a.url,
            is_published=True,
            datetime_created=a.date,
        )
        item.save()
        articles.append(a)

    return articles


def main():
    """Test run scraper by printing all articles."""
    articles = Article.fetch_all()
    print(f"Found {len(articles)} articles:")
    for a in articles:
        print(a)


if __name__ == '__main__':
    main()
