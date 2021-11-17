"""Models for storing event content.

django_timezone_field: https://github.com/mfogel/django-timezone-field
"""

from django.db import models
from django.db.models import JSONField
from django.template.defaultfilters import slugify
from django.conf import settings
from urllib.parse import urljoin
from timezone_field import TimeZoneField

from utils.filters import get_blurb_from_markdown


def get_event_image_path(instance, filename):
    """Return media path for uploaded images."""
    return f"uploads/events/{instance.event.id}/{filename}"


class Tag(models.Model):
    """A tag for event and news items.

    N.b. Use <input type="color"> for color widget.
    """

    name = models.CharField(max_length=20)
    color = models.CharField(max_length=7)  # Hex color
    material_icon = models.CharField(
        max_length=50, null=True, blank=True,
        help_text=('A valid material design icon identifier.'
                   ' See: https://fonts.google.com/icons')
    )
    archived = models.BooleanField(default=False)

    def __str__(self):
        """Return string representation."""
        return self.name

    def font_color(self):
        """Return appropriate font color for selected background."""
        rgb = tuple(int(self.color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        if sum(rgb) > 400:
            return "#333"
        return "#fff"


class Supporter(models.Model):
    """A supporter/sponsor of event and news items."""

    name = models.CharField(max_length=50)
    url = models.URLField()
    logo = models.FileField(
        upload_to='logos',  # subdir in MEDIA_ROOT
    )
    archived = models.BooleanField(default=False)

    def __str__(self):
        """Return string representation."""
        return self.name

    @property
    def logo_uri(self):
        """Return media URI for logo."""
        return urljoin(settings.MEDIA_URL, str(self.logo))


class Event(models.Model):
    """An event relevant to the Galaxy users.

    Icons must be strings matching material icon identifier.
    """

    datetime_created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    body = models.CharField(
        max_length=50000, null=True, blank=True,
        help_text=(
            """Enter valid markdown.
            Add event images at the bottom of the page, and tag them
            in markdown like so:
            <pre> ![alt text](img1) <br> ![alt text](img2) </pre>"""
        )
    )
    organiser_name = models.CharField(max_length=100, null=True, blank=True)
    organiser_email = models.EmailField(max_length=255, null=True, blank=True)
    address = JSONField(null=True, blank=True, help_text="Valid JSON string")

    timezone = TimeZoneField(
        default="Australia/Sydney",
        choices_display='WITH_GMT_OFFSET',
        null=True,
        blank=True,
    )
    date_start = models.DateField(null=True, blank=True)
    date_end = models.DateField(null=True, blank=True)
    time_start = models.TimeField(null=True, blank=True)
    time_end = models.TimeField(null=True, blank=True)

    external = models.URLField(
        null=True, blank=True, help_text='Link to external content')

    tags = models.ManyToManyField(Tag, blank=True)
    supporters = models.ManyToManyField(
        Supporter, blank=True, help_text='Displays logos and links')

    @property
    def url(self):
        """Return internal or external link."""
        return (
            self.external
            or f'/events/{self.id}'
        )

    @property
    def slug(self):
        """Return slug generated from title."""
        return slugify(self.title)

    @property
    def ics_url(self):
        """Return URL for calendar ICS file."""
        return urljoin(settings.HOSTNAME, f'event/{self.id}/{self.slug}.ics')

    @property
    def material_icons(self):
        """Return list of material icon identifiers for event."""
        return [
            x.material_icon
            for x in self.tags.filter(material_icon__isnull=False)
        ]

    @property
    def blurb(self):
        """Extract a blurb from the body markdown."""
        return get_blurb_from_markdown(self.body, style=False)


class EventImage(models.Model):
    """An image to embed in an event article."""

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.FileField(
        upload_to=get_event_image_path,
    )

    @property
    def img_uri(self):
        """Return media URI for logo."""
        return urljoin(settings.MEDIA_URL, str(self.image))
