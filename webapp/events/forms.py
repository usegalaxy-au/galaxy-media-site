"""Forms for managing events.

django_timezone_field: https://github.com/mfogel/django-timezone-field
"""

from django import forms
from timezone_field import TimeZoneFormField


class EventForm(forms.Form):
    """Create a new event."""

    # Displays like "GMT-08:00 America/Los Angeles"
    timezone = TimeZoneFormField(choices_display='WITH_GMT_OFFSET')
