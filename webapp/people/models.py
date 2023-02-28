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
    location = models.CharField(max_length=255, null=True, blank=True)
    github = models.CharField(max_length=100, null=True, blank=True)
    gitter = models.CharField(max_length=100, null=True, blank=True)
    twitter = models.CharField(max_length=100, null=True, blank=True)
    orcid = models.CharField(max_length=19, null=True, blank=True)
    bio = models.CharField(max_length=600, null=True, blank=True)
    ranking = models.IntegerField(blank=True, default=99, help_text=(
        "Profiles are ordered first by ascending rank, and then by date"
        " created (oldest first). To order by date created, leave the default"
        " of 99.")
    )
    image = models.ImageField(
        upload_to='people',
        null=True,
        blank=True,
    )
    alumni = models.BooleanField(default=False)

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
        if self.image:
            return urljoin(settings.MEDIA_URL, str(self.image))
        return urljoin(settings.STATIC_URL, 'people/img/placeholder.png')
