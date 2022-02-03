"""User-facing forms for making content requests (tools/data)."""


from django import forms
from crispy_forms.helper import FormHelper


class ResourceRequestForm(forms.Form):
    """Form for requesting a tool or dataset."""

    # For crispy bootstrap4 forms
    helper = FormHelper()

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

    def clean(self):
        """Validate and clean the dispatched form."""
        pass

    def dispatch(self):
        """Dispatch the form content as an email."""
        pass


class QuotaRequestForm(forms.Form):
    """Form for requesting data quota."""

    pass


class SupportRequestForm(forms.Form):
    """Form for requesting user support. Is this required?"""

    pass
