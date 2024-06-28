import requests
import requests_mock
from django.test import Client
from django.core.files import File
from django.core import mail
from pathlib import Path

from .lab_export import ExportSubsiteContext
from .models import Notice, Subsite
from .test.data import (
    TEST_NOTICES,
    TEST_LABS,
    MOCK_REQUESTS,
    MOCK_LAB_BASE_URL,
)
from events.models import Event, Supporter, Tag
from events.test.data import TEST_EVENTS, TEST_SUPPORTERS, TEST_TAGS
from news.models import News
from news.test.data import TEST_NEWS
from utils import institution
from utils.data.fgenesh import genematrix_tree
from webapp.test import TestCase

TEST_DATA_DIR = Path(__file__).parent / 'test/data'
TEST_LAB_NAME = 'Antarctica'
TEST_LAB_LAB_NAME = 'Galaxy Lab Pages'.upper()
TEST_LAB_NATIONALITY = 'Antarctican'
TEST_LAB_GALAXY_BASE_URL = 'https://galaxy-antarctica.org'
TEST_LAB_SECTION_TEXT = 'Example section'
TEST_LAB_ACCORDION_TEXT = (
    'Report statistics from sequencing reads',
    'Assemble Nanopore long reads.',
)
TEST_LAB_CONTENT_URL = f'{MOCK_LAB_BASE_URL}/static/home/labs/docs/main.yml'
TEST_LAB_URL = f'/lab/export?content_root={TEST_LAB_CONTENT_URL}'


def test_lab_url_for(lab):
    """Return the URL for the given lab name."""
    return TEST_LAB_URL.replace('docs', lab)


class HomeTestCase(TestCase):

    def setUp(self) -> None:
        """Create some data to request a landing page."""
        super().setUp()
        self.client = Client()

        for subsite in TEST_LABS[1:]:
            # First TEST_LAB "main" is created on DB migration
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

    def test_subsite_landing_webpage(self):
        response = self.client.get(f'/landing/{TEST_LABS[1]["name"]}')
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

    def test_utility_institution(self):
        assert institution.is_institution_email('johndoe@uq.edu.au')
        assert not institution.is_institution_email('johndoe@gmail.com')
        # Subdomain matching
        assert institution.is_institution_email('johndoe@sub1.uq.edu.au')
        assert not institution.is_institution_email('johndoe@gmail.edu.au')


class LabExportTestCase(TestCase):
    """Test exported lab site building functionality."""

    @requests_mock.Mocker()
    def setUp(self, mock_request):
        for url, text in MOCK_REQUESTS.items():
            mock_request.get(url, text=text, status_code=200)
        self.context = ExportSubsiteContext(TEST_LAB_CONTENT_URL)

    def test_it_can_make_raw_url(self):
        self.assertEqual(
            self.context._make_raw('https://github.com/usegalaxy-au/'
                                   'galaxy-media-site/blob/dev/README.md'),
            'https://raw.githubusercontent.com/usegalaxy-au/'
            'galaxy-media-site/dev/README.md')

    @requests_mock.Mocker()
    def test_exported_lab_docs(self, mock_request):
        """Mock requests to localhost."""
        for url, text in MOCK_REQUESTS.items():
            mock_request.get(url, text=text, status_code=200)
        response = self.client.get(TEST_LAB_URL)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, TEST_LAB_NAME)
        self.assertContains(response, TEST_LAB_LAB_NAME)
        self.assertContains(response, TEST_LAB_GALAXY_BASE_URL)
        self.assertContains(response, TEST_LAB_SECTION_TEXT)
        for text in TEST_LAB_ACCORDION_TEXT:
            self.assertContains(response, text)

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
            'matrices': [genematrix_tree.as_choices()[0][0]],
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
