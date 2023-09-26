from django.test import Client
from django.core.files import File
from unittest import mock
from types import SimpleNamespace

from webapp.test import TestCase
from events.test.data import TEST_SUPPORTERS, TEST_TAGS
from events.models import Supporter, Tag
from home.test.decorators import suppress_request_warnings
from .models import News, APIToken
from .scrape import biocommons, hub
from .test.data import HUB_JSON, MOCK_REQUESTS, TEST_NEWS


class MockResponse:
    def __init__(self, data=None, html=None, status_code=200):
        self.json_data = data
        self.html_data = html
        self.status_code = status_code
        self.content = SimpleNamespace(decode=lambda x: self.html_data)

    def raise_for_status(self):
        pass

    def json(self):
        return self.json_data


def mocked_requests_get(*args, **kwargs):
    """Not sure if mock is necessary or just use a real requests.get."""
    url = args[0]
    if url in MOCK_REQUESTS:
        content = MOCK_REQUESTS[url]
        if isinstance(content, dict):
            return MockResponse(data=content)
        return MockResponse(html=content)
    return MockResponse(None, 404)


class NewsTestCase(TestCase):

    def setUp(self) -> None:
        """Create some data."""
        super().setUp()
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
                supporter = Supporter.objects.get(
                    name=supporter['data']['name'])
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
        response = self.client.post('/news/api/create', {
            'api_token': key.token,
            'body': TEST_NEWS[2]['data']['body'],
            'tool_update': 'true',
        })
        self.assertEqual(response.status_code, 201)
        news_item = News.objects.filter(is_tool_update=True).last()
        assert "### Tools installed" in news_item.body, (
            f'"### Tools installed" not found in string:\n{news_item.body}'
        )

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_biocommons_news_web_scraper(self, mock_get):
        articles = biocommons.Article.fetch_all()
        assert len(articles) > 0, "No articles scraped from BioCommons webpage"
        # assert article content

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_hub_news_scraper(self, mock_get):
        articles = hub.Article.fetch_all()
        self.assertEquals(
            len(articles),
            3,
            f"Scraped {len(articles)} from Hub JSON feed but expected 3."
        )
        for i, a in enumerate(articles):
            expected = HUB_JSON['news'][i]
            self.assertEquals(
                a.title,
                expected['title'],
            )
            self.assertEquals(
                a.url,
                hub.BASE_URL + expected['path'],
            )
            self.assertEquals(
                a.date.strftime('%-d %B %Y'),
                expected['date'],
            )
