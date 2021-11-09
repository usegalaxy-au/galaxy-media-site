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

    def __str__(self):
        """Return string representation."""
        return self.name


class Supporter(models.Model):
    """A supporter/sponsor of event and news items."""

    name = models.CharField(max_length=50)
    url = models.URLField()
    logo = models.FileField(
        upload_to='logos',  # subdir in MEDIA_ROOT
    )

    def __str__(self):
        """Return string representation."""
        return self.name


class Event(models.Model):
    """An event relevant to the Galaxy users.

    Icons must be strings matching material icon identifier.
    """

    datetime_created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    body = models.CharField(
        max_length=10000, null=True, blank=True,
        help_text='Enter valid markdown')
    organiser_name = models.CharField(max_length=100, null=True, blank=True)
    organiser_email = models.EmailField(max_length=255, null=True, blank=True)
    address = JSONField(null=True, blank=True)

    timezone = TimeZoneField(
        default="Australia/Sydney",
        choices_display='WITH_GMT_OFFSET',
    )
    date_start = models.DateField(null=True, blank=True)
    date_end = models.DateField(null=True, blank=True)
    time_start = models.TimeField(null=True, blank=True)
    time_end = models.TimeField(null=True, blank=True)

    external = models.URLField(
        null=True, blank=True, help_text='Link to external content')

    tags = models.ManyToManyField(Tag)
    supporters = models.ManyToManyField(
        Supporter, help_text='Show logos/links')

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
        return [x.icon for x in self.tags]

    @property
    def blurb(self):
        """Extract a blurb from the body markdown."""
        return get_blurb_from_markdown(self.body)
