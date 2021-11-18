"""Models for storing event content."""

from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from urllib.parse import urljoin

from events.models import Tag, Supporter
from utils.markdown import get_blurb_from_markdown


def get_upload_dir(instance, filename):
    """Return media path for uploaded images."""
    return f"uploads/events/{instance.news.id}/{filename}"


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
        help_text=(
            """Enter valid GitHub markdown.
            Add news images at the bottom of the page, and tag them
            in markdown like so:
            <pre> ![alt text](img1) <br> ...<br> ![alt text](img2) </pre>"""
        )
    )
    external = models.URLField(
        null=True,
        blank=True,
        help_text=(
            'Link to external content. Users will be directed here instead'
            ' of the post page, so use instead of body.')
    )
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


class NewsImage(models.Model):
    """An image to embed in an event article."""

    news = models.ForeignKey(
        News,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.FileField(
        upload_to=get_upload_dir,
    )

    @property
    def img_uri(self):
        """Return media URI for logo."""
        return urljoin(settings.MEDIA_URL, str(self.image))
