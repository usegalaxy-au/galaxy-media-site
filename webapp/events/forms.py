"""Forms for managing events."""

from django import forms

from home.widgets import ColorInput
from .models import Event, Tag


class EventAdminForm(forms.ModelForm):
    """Update and create events."""

    class Meta:
        """Form metadata."""

        model = Event
        widgets = {
            'body': forms.Textarea(attrs={
                'rows': 10,
                'cols': 80,
            }),
        }
        fields = '__all__'


class TagAdminForm(forms.ModelForm):
    """Update and create tags."""

    class Meta:
        """Form metadata."""

        model = Tag
        widgets = {
            'color': ColorInput,
        }
        fields = '__all__'
