"""Models for storing event content."""

import os
import uuid
from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from urllib.parse import urljoin

from events.models import Tag, Supporter
from utils.markdown import (
    get_blurb_from_markdown,
    render_image_uri,
    MARKDOWN_HELP_TEXT,
    MARKDOWN_IMAGE_HELP_TEXT,
)


def get_upload_dir(instance, filename):
    """Return media path for uploaded images."""
    return f"uploads/news/{instance.news.id}/{filename}"


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
        help_text=MARKDOWN_HELP_TEXT + MARKDOWN_IMAGE_HELP_TEXT,
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
    is_published = models.BooleanField(default=False)
    is_tool_update = models.BooleanField(default=False)

    def __str__(self):
        """Return string definition."""
        return f'News item <{self.id}> "{self.title}"'

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

    def render_markdown_uris(self):
        """Render NewsImage URIs into markdown placeholders."""
        images = NewsImage.objects.filter(news_id=self.id).order_by('id')
        new_body = render_image_uri(self.body, images)
        if new_body != self.body:
            # Avoid the dreaded infinite loop - only save if body changed
            self.body = new_body
            self.save()


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

    def __str__(self):
        """Return string representation."""
        return os.path.basename(str(self.image))

    @property
    def img_uri(self):
        """Return media URI for logo."""
        return urljoin(settings.MEDIA_URL, str(self.image))


class APIToken(models.Model):
    """Tokens for accessing the news API."""

    token = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(max_length=100, help_text="A name for this token.")

    def __str__(self):
        """Return string representation."""
        return f'API token: {self.name}'

    @classmethod
    def matches(cls, token):
        """Test whether the given token matches database."""
        registered_tokens = [
            str(x)
            for x in cls.objects.values_list('token', flat=True)
        ]
        if token in registered_tokens:
            return True
        return False
