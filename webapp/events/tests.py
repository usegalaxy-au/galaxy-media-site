from django.test import Client
from django.core.files import File

from webapp.test import TestCase
from home.test.decorators import suppress_request_warnings
from .models import Event, EventImage, Supporter, Tag
from .test.data import TEST_EVENTS, TEST_SUPPORTERS, TEST_TAGS, TEST_IMAGES


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

    def test_image_uri_is_rendered_in_markdown_body(self):
        event = Event.objects.get(title=TEST_EVENTS[3]['data']['title'])
        event_images = []
        for image in TEST_IMAGES:
            e = EventImage(event=event)
            with open(image, 'rb') as i:
                e.image.save(
                    image.name,
                    File(i)
                )
            event_images.append(e)

        # Image URIs should now be rendered in event.body markdown
        event = Event.objects.get(title=TEST_EVENTS[3]['data']['title'])
        for image in event_images:
            assert f"({image.img_uri})" in event.body, (
                "EventImage URI was not found in event.body markdown:"
                f" '{image.img_uri}'\n\n"
                ">>> event.body:\n\n"
                f"{event.body}"
            )
        assert (
            event.body.index(event_images[0].img_uri)
            < event.body.index(event_images[1].img_uri)
        ), (
            "EventImage URIs have rendered out-of-order in markdown:\n"
            f"{event.body}"
        )
