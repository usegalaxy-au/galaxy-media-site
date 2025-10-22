import requests
from django.test import Client
from django.core.files import File
from django.core import mail
from pathlib import Path

from .models import Notice
from .test.data import TEST_NOTICES
from events.models import Event, Supporter, Tag
from events.test.data import TEST_EVENTS, TEST_SUPPORTERS, TEST_TAGS
from news.models import News
from news.test.data import TEST_NEWS
from utils import institution
from webapp.test import TestCase

TEST_DATA_DIR = Path(__file__).parent / 'test/data'

# Endpoints to test for HTTP 200
TEST_ENDPOINTS = [
    '/about',
    '/request',
    '/request/tool',
    '/request/quota',
    '/request/support',
    '/request/access',
    '/list-of-institutions.html',
]


class HomeTestCase(TestCase):

    def setUp(self) -> None:
        """Create some data to request a landing page."""
        super().setUp()
        self.client = Client()
        for notice in TEST_NOTICES:
            notice = Notice.objects.create(**notice['data'])
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
        for event in TEST_EVENTS:
            tags = event['relations']['tags']
            supporters = event['relations']['supporters']
            event = Event.objects.create(**event['data'])
            for tag in tags:
                tag = Tag.objects.get(name=tag['name'])
                event.tags.add(tag)
            for supporter in supporters:
                supporter = Supporter.objects.get(
                    name=supporter['data']['name'])
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
            "window.location = '/news/",
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

    def test_aaf_webpage(self):
        try:
            response = self.client.get('/aaf')
        except requests.exceptions.ConnectionError:
            print('\nNo internet connection - cannot test AAF list.')
            return

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            'University of Queensland'
        )

    def test_webpages(self):
        for endpoint in TEST_ENDPOINTS:
            response = self.client.get(endpoint)
            self.assertLess(response.status_code, 300)

    def test_utility_institution(self):
        assert institution.is_institution_email('johndoe@uq.edu.au')
        assert not institution.is_institution_email('johndoe@gmail.com')
        # Subdomain matching
        assert institution.is_institution_email('johndoe@sub1.uq.edu.au')
        assert not institution.is_institution_email('johndoe@gmail.edu.au')

    def test_embedded_snippets(self):
        response = self.client.get('/embed/home/snippets/footer.html')
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            '</footer>',
        )


class AccessRequestsTestCase(TestCase):

    def test_it_can_show_alphafold_access_form(self):
        response = self.client.get('/request/access/alphafold')
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            'AlphaFold 2 Access Request',
        )

    def test_it_can_handle_request_for_alphafold_access(self):
        response = self.client.post('/request/access/alphafold', {
            'name': 'John Doe',
            'email': 'test@uq.edu.au',
        })
        self.assert_access_form_success(response, auto_action=True)

    def test_it_can_handle_request_for_fgenesh_access(self):
        response = self.client.post('/request/access/fgenesh', {
            'name': 'John Doe',
            'email': 'test@uq.edu.au',
            'agree_terms': 'on',
            'agree_acknowledge': 'on',
        })
        self.assert_access_form_success(response, auto_action=False)

    def test_it_can_handle_request_for_cellranger_access(self):
        response = self.client.post('/request/access/cellranger', {
            'name': 'John Doe',
            'email': 'test@uq.edu.au',
            'agree_terms': 'on',
            'agree_usage': 'on',
        })
        self.assert_access_form_success(response, auto_action=True)

    def assert_access_form_success(self, response, auto_action=True):
        """Assert that an auto-action form has been successfully submitted.

        Auto-action forms send an email to user to let them know that access
        has been granted. Non-auto-action forms do not send an email because
        manual intervention is required.
        """
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            'Thanks for your submission',
        )
        if auto_action:
            self.assertContains(
                response,
                'please check your spam folder',
            )
        else:
            self.assertNotContains(
                response,
                'please check your spam folder',
            )
        expect_len = 2 if auto_action else 1
        self.assertEqual(len(mail.outbox), expect_len)
