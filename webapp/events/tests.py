from django.test import TestCase
from django.test import Client
from django.core.files import File

from home.test.decorators import suppress_request_warnings
from .models import Event, Supporter, Tag
from .test.data import TEST_EVENTS, TEST_SUPPORTERS, TEST_TAGS


class EventsTestCase(TestCase):

    def setUp(self) -> None:
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

    def test_event_webpage(self):
        event = Event.objects.get(title=TEST_EVENTS[0]['data']['title'])
        response = self.client.get(f'/events/{event.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            event.title,
        )

    @suppress_request_warnings
    def test_unpublished_webpage_404(self):
        unpublished_event = Event.objects.get(title=TEST_EVENTS[1]['data']['title'])
        response = self.client.get(f'/events/{unpublished_event.id}/')
        self.assertEqual(response.status_code, 404)
