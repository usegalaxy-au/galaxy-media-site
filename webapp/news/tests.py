from django.test import TestCase
from django.test import Client
from django.core.files import File

from events.test.data import TEST_SUPPORTERS, TEST_TAGS
from events.models import Supporter, Tag
from home.test.decorators import suppress_request_warnings
from .models import News, APIToken
from .scrape import biocommons
from .test.data import TEST_NEWS


class NewsTestCase(TestCase):

    def setUp(self) -> None:
        """Create some data."""
        self.client = Client()
        for tag in TEST_TAGS:
            Tag.objects.create(**tag)
        for supporter in TEST_SUPPORTERS:
            s = Supporter.objects.create(**supporter['data'])
            with open(supporter['files']['logo'], 'rb') as logo:
                s.logo.save(
                    supporter['files']['logo'].name,
                    File(logo)
                )
        for news_item in TEST_NEWS:
            tags = news_item['relations']['tags']
            supporters = news_item['relations']['supporters']
            news_item = News.objects.create(**news_item['data'])
            for tag in tags:
                tag = Tag.objects.get(name=tag['name'])
                news_item.tags.add(tag)
            for supporter in supporters:
                supporter = Supporter.objects.get(name=supporter['data']['name'])
                news_item.supporters.add(supporter)


    def test_news_article_webpage(self):
        article = News.objects.get(title=TEST_NEWS[0]['data']['title'])
        response = self.client.get(f'/news/{article.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            article.title,
        )

    @suppress_request_warnings
    def test_unpublished_article_404(self):
        unpublished_article = News.objects.get(
            title=TEST_NEWS[1]['data']['title']
        )
        response = self.client.get(f'/news/{unpublished_article.id}/')
        self.assertEqual(response.status_code, 404)

    def test_tool_update_api(self):
        key = APIToken.objects.create(name="key")
        response = self.client.post(
            '/news/api/create',
            {
                'api_token': key.token,
                'body': TEST_NEWS[2]['data']['body'],
                'tool_update': 'true',
            },
        )
        self.assertEqual(response.status_code, 201)
        news_item = News.objects.filter(is_tool_update=True).last()
        assert "### Tools installed" in news_item.body, (
            f'"### Tools installed" not found in string:\n{news_item.body}'
        )

    def test_biocommons_news_web_scraper(self):
        articles = biocommons.Article.fetch_all()
        assert len(articles) > 0, "No articles scraped from BioCommons webpage"
