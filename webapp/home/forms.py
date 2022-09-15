"""User facing forms for making support requests (help/tools/data)."""

import logging
import traceback
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from captcha import fields
from utils.institution import is_institution_email
from . import validators


logger = logging.getLogger('django')


def dispatch_form_mail(
        to_address=None,
        reply_to=None,
        subject=None,
        text=None,
        html=None):
    """Send mail to support inbox.

    This should probably be sent to a worker thread/queue.
    """
    logger.info(f"Sending mail to {settings.EMAIL_TO_ADDRESS}")
    reply_to_value = [reply_to] if reply_to else None
    email = EmailMultiAlternatives(
        subject,
        text,
        to_address or settings.EMAIL_FROM_ADDRESS,
        [to_address],
        reply_to=reply_to_value,
    )
    if html:
        email.attach_alternative(html, "text/html")

    tries = 0
    while True:
        try:
            email.send()
            return
        except Exception:
            logger.warning(f"Send mail error - attempt {tries}")
            tries += 1
            if tries < 3:
                continue
            logger.error(
                "Error sending mail. The user did not receive an error.\n"
                + traceback.format_exc()
                + f"\n\nMail content:\n\n{text}"
            )
            return


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

    # Fields for tool
    tool_toolshed_available = forms.BooleanField(required=False)
    tool_toolshed_url = forms.URLField(required=False)
    tool_test_data = forms.BooleanField(required=False)

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

    name = forms.CharField()
    email = forms.EmailField()
    start_date = forms.DateField()
    duration_months = forms.IntegerField()
    disk_tb = forms.IntegerField()
    disk_tb_other = forms.IntegerField(required=False)
    description = forms.CharField()
    captcha = fields.ReCaptchaField()
    accepted_terms = forms.BooleanField()

    def clean(self):
        """Validate and check 'other' values."""
        data = super().clean()
        # These fields have an "other" option with text input
        OTHER_FIELDS = [
            'disk_tb',
        ]
        for field in OTHER_FIELDS:
            if not data.get(field):
                # User may have selected the 'other' field and typed a value
                if not data.get(f'{field}_other'):
                    if self.fields[field].required:
                        self.add_error(
                            field,
                            ValidationError('This field is required'))
                        continue
                other_value = data.get(f'{field}_other')
                if type(other_value) == str:
                    data[field] = 'Other - ' + other_value
                else:
                    data[field] = other_value
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


class AlphafoldRequestForm(forms.Form):
    """Form to request AlphaFold access."""

    name = forms.CharField()
    email = forms.EmailField(validators=[validators.institutional_email])
    institution = forms.CharField()
    species = forms.CharField(required=False)
    domain = forms.CharField(required=False)
    proteins = forms.CharField(required=False)
    size_aa = forms.IntegerField(required=False)
    count_aa = forms.IntegerField(required=False)

    def clean_email(self):
        """Validate email address."""
        email = self.cleaned_data['email']
        if not is_institution_email(email):
            raise ValidationError(
                (
                    'Sorry, this is not a recognised Australian institute'
                    ' email address.'
                ),
                field="email",
            )
        return email

    def dispatch(self):
        """Dispatch form content as email."""
        template = 'home/requests/mail/alphafold'
        dispatch_form_mail(
            reply_to=self.cleaned_data['email'],
            subject="New AlphaFold request on Galaxy Australia",
            text=render_to_string(f'{template}.txt', {'form': self}),
            html=render_to_string(f'{template}.html', {'form': self}),
        )

    def dispatch_warning(self):
        """Dispatch warning email to let user know their email is invalid."""
        template = 'home/requests/mail/alphafold-email-invalid'
        dispatch_form_mail(
            to_address=self.cleaned_data['email'],
            subject="Access to AlphaFold could not be granted",
            text=render_to_string(f'{template}.txt', {'form': self}),
            html=render_to_string(f'{template}.html', {'form': self}),
        )
