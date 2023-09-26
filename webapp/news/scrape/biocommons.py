"""Scrape Galaxy news from the BioCommons."""

import logging
import requests
import traceback
from datetime import datetime
from bs4 import BeautifulSoup
from django.utils import timezone
from news.models import News

logger = logging.getLogger('django')

BASE_URL = 'https://www.biocommons.org.au'
URL = f'{BASE_URL}/news/category/Galaxy+Australia+news'


class Article:
    """A new item scraped from the BioCommons website."""

    def __init__(self, soup):
        """Create news item from web content."""
        self.url = BASE_URL + soup.find(
            'a',
            class_='BlogList-item-readmore',
        )['href']
        self.title = soup.find(
            'a',
            class_='BlogList-item-title',
        ).text.strip(' \n\t')
        self.date = timezone.make_aware(datetime.strptime(
            soup.find('time')['datetime'],
            '%Y-%m-%d',
        ))

    def __str__(self):
        """Return string representation."""
        return f"Article {self.date.strftime('%Y-%m-%d')}: {self.title}"

    @classmethod
    def fetch_all(cls):
        """Fetch and parse all current news items."""
        html = requests.get(URL).content.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        articles = []
        for article_soup in soup.find_all('article'):
            try:
                articles.append(cls(article_soup))
            except Exception:
                logger.error("Error parsing BioCommons news article")
                logger.error(traceback.format_exc())
                logger.error("SOUP:")
                logger.error(str(article_soup))

        return articles


def fetch_articles():
    """Fetch articles and add new ones to the database."""
    articles = []
    for a in Article.fetch_all():
        if News.objects.filter(external=a.url).count():
            # This news item already exists
            continue
        item = News.objects.create(
            title=a.title,
            external=a.url,
            is_published=True,
        )
        item.datetime_created = a.date
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
