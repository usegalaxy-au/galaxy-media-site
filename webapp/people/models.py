"""Models for storing people data."""

from urllib.parse import urljoin
from django.db import models
from django.conf import settings


class Person(models.Model):
    """A Galaxy AU team member."""

    class Meta:
        """Class metadata."""

        verbose_name_plural = "people"

    datetime_created = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    position = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    github = models.CharField(max_length=100, null=True, blank=True)
    gitter = models.CharField(max_length=100, null=True, blank=True)
    twitter = models.CharField(max_length=100, null=True, blank=True)
    orcid = models.CharField(max_length=19, null=True, blank=True)
    bio = models.CharField(max_length=600, null=True, blank=True)
    image = models.ImageField(
        upload_to='people',
        null=True,
        blank=True,
    )

    def __str__(self):
        """Return string representation."""
        return self.full_name

    @property
    def full_name(self):
        """Return full name."""
        return f"{self.first_name} {self.last_name}"

    @property
    def img_uri(self):
        """Return URI for image field."""
        return urljoin(settings.MEDIA_URL, str(self.image))
