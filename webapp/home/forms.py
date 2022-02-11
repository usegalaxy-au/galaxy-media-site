"""User facing forms for making support requests (help/tools/data)."""

import logging
import traceback
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from captcha import fields

logger = logging.getLogger(__name__)


def dispatch_form_mail(reply_to=None, subject=None, text=None, html=None):
    """Send mail to support inbox.

    This should probably be sent to a worker thread/queue.
    """
    logger.info(f"Sending mail to {settings.EMAIL_TO_ADDRESS}")
    email = EmailMultiAlternatives(
        subject,
        text,
        settings.EMAIL_FROM_ADDRESS,
        [settings.EMAIL_TO_ADDRESS],
        reply_to=[reply_to],
    )
    if html:
        email.attach_alternative(html, "text/html")
    try:
        email.send()
    except Exception:
        logger.error("Error sending mail:\n" + traceback.format_exc())


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

    def dispatch(self):
        """Dispatch form content as email."""
        data = self.cleaned_data
        template = (
            'home/requests/mail/'
            f"{data['resource_type']}"
        )
        dispatch_form_mail(
            reply_to=data['email'],
            subject=(
                f"New {data['resource_type']}"
                " request on Galaxy Australia"
            ),
            text=render_to_string(f'{template}.txt', {'form': self}),
            html=render_to_string(f'{template}.html', {'form': self}),
        )


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
        # These fields have an "other" option with text input
        OTHER_FIELDS = [
            'organism',
            'technology',
            'file_type',
            'max_samples',
        ]
        # These values for "organism" link to the "other" text input too
        ORGANISM_OTHER_VALUES = [
            'bacteria',
            'plant',
        ]

        for field in OTHER_FIELDS:
            if not data.get(field):
                # User may have selected the 'other' field and typed a value
                if not data.get(f'{field}_other'):
                    self.add_error(
                        field,
                        ValidationError('This field is required'))
                other_value = data.get(f'{field}_other')
                if type(other_value) == str:
                    data[field] = 'Other - ' + other_value
                else:
                    data[field] = other_value

        for value in ORGANISM_OTHER_VALUES:
            if data.get('organism') == value:
                data['organism'] = (
                    f"{value.title()} - {data['organism_other']}")

        return data

    def dispatch(self):
        """Dispatch form content as email."""
        template = 'home/requests/mail/quota'
        dispatch_form_mail(
            reply_to=self.cleaned_data['email'],
            subject="New Quota request on Galaxy Australia",
            text=render_to_string(f'{template}.txt', {'form': self}),
            html=render_to_string(f'{template}.html', {'form': self}),
        )


class SupportRequestForm(forms.Form):
    """Form to request for user support."""

    name = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField()

    def dispatch(self):
        """Dispatch content via the FreshDesk API."""
        data = self.cleaned_data
        dispatch_form_mail(
            reply_to=data['email'],
            subject="Galaxy Australia Support request",
            text=(
                f"Name: {data['name']}\n"
                f"Email: {data['email']}\n\n"
                + data['message']
            )
        )
