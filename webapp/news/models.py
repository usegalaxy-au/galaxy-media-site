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
    body = models.CharField(max_length=10000, null=True)
    external = models.URLField(null=True)
    tags = models.ManyToManyField(Tag)
    supporters = models.ManyToManyField(Supporter)

    @property
    def slug(self):
        """Return slug generated from title."""
        return slugify(self.title)

    @property
    def material_icons(self):
        """Return list of material icon identifiers for event."""
        return [x.icon for x in self.tags]

    @property
    def blurb(self):
        """Extract a blurb from the body markdown."""
        return get_blurb_from_markdown(self.body)
