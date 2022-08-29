"""Scrape news articles from BioCommons website."""

from django.core.management.base import BaseCommand
from news.scrape import biocommons


class Command(BaseCommand):
    """Django manage.py command for running news article scraper."""

    help = (
        'Fetch news articles from the BioCommons website and add them to the'
        ' database as external news articles.'
    )

    def handle(self, *args, **kwargs):
        """Run the command."""
        print("Fetching news articles...")
        articles = biocommons.fetch_articles()
        print(f"Added {len(articles)} articles to the database:")
        for a in articles:
            print(a)
