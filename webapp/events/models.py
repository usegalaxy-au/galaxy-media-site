"""Models for storing event content."""

import os
from django.db import models
from django.template.defaultfilters import slugify
from django.conf import settings
from timezone_field import TimeZoneField
from urllib.parse import urljoin

from utils.markdown import (
    get_blurb_from_markdown,
    render_image_uri,
    MARKDOWN_HELP_TEXT,
    MARKDOWN_IMAGE_HELP_TEXT,
)


def get_upload_dir(instance, filename):
    """Return media path for uploaded images."""
    return f"uploads/events/{instance.event.id}/{filename}"


def default_address():
    """Return default value for address field."""
    return {
        'name': None,
        'street': None,
        'city': None,
        'region': None,
        'country': None,
    }


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


class EventLocation(models.Model):
    """A location to be associated with events."""

    FIELDS = [
        'name',
        'street',
        'city',
        'region',
        'country',
        'postal',
    ]

    name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text=(
            "All fields are optional."
            " Only populated fields will be displayed."),
    )
    street = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    postal = models.CharField(max_length=20, null=True, blank=True)
    archived = models.BooleanField(default=False)

    def __str__(self):
        """Return string representation."""
        return self.name or self.street or f"Event location ({self.id})"

    @property
    def fields(self):
        """Return list of fields with values."""
        fields = []
        for f in self.FIELDS:
            v = getattr(self, f)
            if v:
                fields.append({
                    'name': f,
                    'value': v,
                })
        return fields

    @property
    def full(self):
        """Return full location as string."""
        loc = []
        for f in self.FIELDS:
            v = getattr(self, f).title()
            if v:
                loc.append(v.replace(',', '\\,'))
        return '\\, '.join(loc)


class Event(models.Model):
    """An event relevant to the Galaxy users.

    Icons must be strings matching material icon identifier.

    Event and News images are saved with the same logic. It's a bit complex
    but seems to be solid and uses inbuilt Django functionality.

    - EventImages are uploaded in the Django admin through the StackedInline
      element.
    - When saved, a post_save hook on EventImage updates the body of the parent
      Event, parsing and rendering image URIs with
      utils.markdown.render_image_uri
    - This function assumes the EventImage number based on the order of saving
    - EventImage order is determined by scanning for the first increment of
      img<n> that matches.

    """

    datetime_created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    body = models.CharField(
        max_length=50000,
        null=True,
        blank=True,
        help_text=MARKDOWN_HELP_TEXT + MARKDOWN_IMAGE_HELP_TEXT,
    )
    organiser_name = models.CharField(max_length=100, null=True, blank=True)
    organiser_email = models.EmailField(max_length=255, null=True, blank=True)
    location = models.ForeignKey(
        EventLocation,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text="This will be rendered as a table.",
    )
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
        null=True,
        blank=True,
        help_text=(
            'Link to external content. Users will be directed here instead'
            ' of the post page, so use instead of body.')
    )

    tags = models.ManyToManyField(
        Tag,
        blank=True,
        help_text="Shown in list (icon) and post views.",
    )
    supporters = models.ManyToManyField(
        Supporter,
        blank=True,
        help_text='Display logos and links for a supporter.',
    )
    is_published = models.BooleanField(default=False)

    @property
    def url(self):
        """Return internal or external link."""
        return (
            self.external
            or f'/events/{self.id}'
        )

    @property
    def address_items(self):
        """Render address items from JSON."""
        if not self.address:
            return
        # Exclude null fields
        return [
            (k, v)
            for k, v in self.address.items()
            if v
        ]

    @property
    def ical_url(self):
        """Return URL for ical file."""
        return f'webcal://{settings.HOSTNAME}/events/{self.id}/ical'

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

    @property
    def datetime_start_str(self):
        """Return string for start date/time."""
        date = self.date_start.strftime("%Y%m%d")
        date += 'T'
        if self.time_start:
            date += self.time_start.strftime("%H%M%S") or '000000'
        else:
            date += '000000'
        return date + 'Z'

    @property
    def datetime_end_str(self):
        """Return string for start date/time."""
        date = self.date_end.strftime("%Y%m%d")
        date += 'T'
        if self.time_end:
            date += self.time_end.strftime("%H%M%S") or '000000'
        else:
            date += '235959'
        return date + 'Z'

    def render_markdown_uris(self):
        """Render EventImage URIs into markdown placeholders."""
        images = EventImage.objects.filter(event_id=self.id).order_by('id')
        new_body = render_image_uri(self.body, images)
        if new_body != self.body:
            # Avoid the dreaded infinite loop - only save if body changed
            self.body = new_body
            self.save()


class EventImage(models.Model):
    """An image to embed in an event article."""

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.FileField(
        upload_to=get_upload_dir,
    )

    def __str__(self):
        """Return string representation."""
        return os.path.basename(str(self.image))

    @property
    def img_uri(self):
        """Return media URI for logo."""
        return urljoin(settings.MEDIA_URL, str(self.image))
