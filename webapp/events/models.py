"""Models for storing event content.

django_timezone_field: https://github.com/mfogel/django-timezone-field
"""

from django.db import models

from timezone_field import TimeZoneField


class Event(models.Model):
    """An event relevant to the Galaxy users."""

    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    body = models.CharField(max_length=10000, null=True)
    organiser_name = models.CharField(max_length=100, null=True)
    organiser_email = models.EmailField(max_length=255, null=True)
    address = models.CharField(max_length=1000, null=True)

    datetime_start = models.DateTimeField()
    datetime_end = models.DateTimeField()
    timezone = TimeZoneField()

    url = models.URLField(null=True)      # Only if external content
    ics_url = models.URLField(null=True)  # Create in pre-save?

    tags = models.ManyToManyField(
        'EventTags',
        on_delete=models.CASCADE,
        null=True,
    )
    supporters = models.ManyToManyField(
        'EventSupporters',
        on_delete=models.CASCADE,
        null=True,
    )


class EventTags(models.Model):
    """A choice of event types.

    Use <input type="color"> field.
    """

    name = models.CharField(max_length=20)
    color = models.CharField(max_length=7)  # Validate for hex color


class EventSupporters(models.Model):
    """A choice of event supporters."""

    name = models.CharField(max_length=20)
    url = models.URLField()
    logo = models.ImageField(
        upload_to='images/logos',  # subdir in MEDIA_ROOT
    )
