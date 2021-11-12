"""Forms for managing news content."""

from django import forms

from .models import News


class NewsAdminForm(forms.ModelForm):
    """Update and create news items."""

    class Meta:
        """Form metadata."""

        model = News
        widgets = {
            'body': forms.Textarea(attrs={
                'rows': 30,
                'cols': 120,
            }),
        }
        fields = '__all__'
