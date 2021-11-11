"""Forms for managing generic content."""

from django import forms

from .models import Notice


class NoticeAdminForm(forms.ModelForm):
    """Update and create events."""

    class Meta:
        """Form metadata."""

        model = Notice
        widgets = {
            'body': forms.Textarea(attrs={
                'rows': 30,
                'cols': 120,
            }),
        }
        fields = '__all__'
