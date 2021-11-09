"""Forms for managing people."""

from django import forms

from .models import Person


class PersonAdminForm(forms.ModelForm):
    """Update and create people."""

    class Meta:
        """Form metadata."""

        model = Person
        widgets = {
            'bio': forms.Textarea,
        }
        fields = '__all__'
