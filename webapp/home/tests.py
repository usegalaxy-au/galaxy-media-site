from django.test import Client
from django.core.files import File
from django.conf import settings

from webapp.test import TestCase
from news.models import News
from news.test.data import TEST_NEWS
from events.models import Event, Supporter, Tag
from events.test.data import TEST_EVENTS, TEST_SUPPORTERS, TEST_TAGS
from utils import institution
from .models import Notice, Subsite
from .test.data import TEST_NOTICES, TEST_SUBSITES


class HomeTestCase(TestCase):

    def setUp(self) -> None:
        """Create some data to request a landing page."""
        self.client = Client()

        for subsite in TEST_SUBSITES[1:]:
            # First TEST_SUBSITE "main" is created on DB migration
            Subsite.objects.create(**subsite)
        for notice in TEST_NOTICES:
            subsites = notice['relations']['subsites']
            notice = Notice.objects.create(**notice['data'])
            for subsite in subsites:
                subsite = Subsite.objects.get(name=subsite['name'])
                notice.subsites.add(subsite)
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
        for event in TEST_EVENTS:
            tags = event['relations']['tags']
            supporters = event['relations']['supporters']
            event = Event.objects.create(**event['data'])
            for tag in tags:
                tag = Tag.objects.get(name=tag['name'])
                event.tags.add(tag)
            for supporter in supporters:
                supporter = Supporter.objects.get(name=supporter['data']['name'])
                event.supporters.add(supporter)

    def test_home_landing_webpage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        # Appropriate notices are being shown
        self.assertContains(
            response,
            # shown as rotating (short) notice:
            TEST_NOTICES[0]['data']['short_description'],
        )
        self.assertNotContains(
            response,
            # shown as rotating (short) notice (should not display body):
            TEST_NOTICES[0]['data']['body'],
        )
        self.assertContains(
            response,
            # shown as rotating (short) notice:
            TEST_NOTICES[1]['data']['short_description'],
        )
        self.assertContains(
            response,
            # shown as block (long) notice:
            TEST_NOTICES[3]['data']['title'],
        )
        self.assertContains(
            response,
            # shown as block (long) notice:
            TEST_NOTICES[3]['data']['body'].split('\n')[-1],
        )
        self.assertNotContains(
            response,
            # unpublished notice:
            TEST_NOTICES[2]['data']['title'],
        )

        # Appropriate news items are being shown
        self.assertContains(
            response,
            TEST_NEWS[0]['data']['title'],
        )
        self.assertNotContains(
            response,
            TEST_NEWS[1]['data']['title'],
        )

        # A tool update link should be shown
        self.assertContains(
            response,
            '''window.location = '/news/''',
            count=1,
        )
        # Should display the date, not the title
        self.assertNotContains(
            response,
            TEST_NEWS[2]['data']['title'],
        )

        # Appropriate events are being shown
        self.assertContains(
            response,
            TEST_EVENTS[0]['data']['title'],
        )
        self.assertContains(
            response,
            TEST_EVENTS[2]['data']['title'],
        )
        self.assertContains(  # external event link
            response,
            f'''window.open('{TEST_EVENTS[2]['data']['external']}')''',
        )
        self.assertNotContains(
            response,
            TEST_EVENTS[1]['data']['title'],
        )

    def test_subsite_landing_webpage(self):
        response = self.client.get(f'/landing/{TEST_SUBSITES[1]["name"]}')
        self.assertEqual(response.status_code, 200)

        # Appropriate notices are being shown
        self.assertContains(
            response,
            TEST_NOTICES[1]['data']['title'],
        )
        self.assertNotContains(
            response,
            TEST_NOTICES[0]['data']['title'],
        )

    def test_aaf_webpage(self):
        response = self.client.get('/aaf')

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            'University of Queensland'
        )

    def test_utility_institution(self):
        assert institution.is_institution_email('johndoe@uq.edu.au')
        assert not institution.is_institution_email('johndoe@gmail.com')
