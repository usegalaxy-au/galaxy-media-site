"""Models for storing event content.

django_timezone_field: https://github.com/mfogel/django-timezone-field
"""

from django.db import models
from django.template.defaultfilters import slugify

from events.models import Tag, Supporter
from utils.filters import get_blurb_from_markdown


class News(models.Model):
    """A news item relevant to Galaxy users."""

    class Meta:
        """Class metadata."""

        verbose_name_plural = "news"

    datetime_created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    body = models.CharField(
        max_length=50000,
        null=True,
        blank=True,
        help_text='Enter valid markdown')
    external = models.URLField(
        null=True,
        blank=True,
        help_text='Link to external content')
    tags = models.ManyToManyField(Tag, blank=True)
    supporters = models.ManyToManyField(
        Supporter,
        blank=True,
        help_text='Show logos/links')

    @property
    def url(self):
        """Return internal or external link."""
        return (
            self.external
            or f'/news/{self.id}'
        )

    @property
    def slug(self):
        """Return slug generated from title."""
        return slugify(self.title)

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
