"""User-facing forms for making content requests (tools/data)."""


from django import forms
from django.core.exceptions import ValidationError
from captcha import fields
from pprint import pprint


class ResourceRequestForm(forms.Form):
    """Form for requesting a tool or dataset."""

    RESOURCE_CHOICES = (
        ('tool', 'Tool'),
        ('dataset', 'Dataset'),
    )

    name = forms.CharField()
    email = forms.EmailField()
    # tool/dataset
    resource_type = forms.ChoiceField(choices=RESOURCE_CHOICES)
    resource_name_version = forms.CharField()
    resource_url = forms.URLField(required=False)
    resource_justification = forms.CharField(required=False)
    resource_research_count = forms.IntegerField(required=False)
    resource_research_groups = forms.CharField(required=False)

    # Fields for tool
    tool_toolshed_available = forms.BooleanField(required=False)
    tool_toolshed_url = forms.URLField(required=False)
    tool_test_data = forms.BooleanField(required=False)

    # Fields for dataset
    dataset_contact_consent = forms.BooleanField(required=False)

    captcha = fields.ReCaptchaField()

    def dispatch(self, html):
        """Dispatch content via the FreshDesk API."""
        print("Dispatch to the FreshDesk API!")
        pprint(self.cleaned_data)
        print(html)


class QuotaRequestForm(forms.Form):
    """Form for requesting data quota."""

    DURATION_MONTHS_CHOICES = (
        ('1', '1 month'),
        ('3', '3 months'),
        ('6', '6 months'),
    )

    name = forms.CharField()
    email = forms.EmailField()
    institution = forms.CharField()
    group_name = forms.CharField()
    start_date = forms.DateField()
    duration = forms.ChoiceField(choices=DURATION_MONTHS_CHOICES)
    disk_gb = forms.IntegerField(required=False)  # null = don't know
    description = forms.CharField()
    organism = forms.CharField(required=False)
    organism_other = forms.CharField(required=False)
    technology = forms.CharField(required=False)
    technology_other = forms.CharField(required=False)
    file_type = forms.CharField(required=False)
    file_type_other = forms.CharField(required=False)
    max_samples = forms.IntegerField(required=False)
    max_samples_other = forms.IntegerField(required=False)
    accepted_terms = forms.BooleanField()

    def clean(self):
        """Validate and check 'other' values."""
        data = super().clean()
        OTHER_FIELDS = [
            'organism',
            'technology',
            'file_type',
            'max_samples',
        ]

        for field in OTHER_FIELDS:
            if not data.get(field):
                # User may have selected the 'other' field and typed a value
                if not data.get(f'{field}_other'):
                    self.add_error(
                        field,
                        ValidationError('This field is required'))
                data[field] = data[f'{field}_other']
        return data

    def dispatch(self):
        """Dispatch content via the FreshDesk API."""
        print("Dispatch to the FreshDesk API!")
        pprint(self.cleaned_data)


class SupportRequestForm(forms.Form):
    """Form to request for user support."""

    name = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField()

    def dispatch(self):
        """Dispatch content via the FreshDesk API."""
        print("Dispatch to the FreshDesk API!")
        pprint(self.cleaned_data)
