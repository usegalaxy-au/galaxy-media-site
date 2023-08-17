"""User facing forms for making support requests (help/tools/data)."""

import logging
import traceback
from captcha import fields
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from utils import galaxy
from utils import postal
from utils.data.fgenesh import genematrix_tree
from utils.institution import is_institution_email

from . import validators

SEND_MAIL_RETRIES = 3
logger = logging.getLogger('django')


def retry_send_mail(mail):
    """Attempt sending email with error log fallback."""
    tries = 0
    while True:
        try:
            if settings.EMAIL_HOST == 'mail.usegalaxy.org.au':
                # Special SMTP setup for GA mail server
                return postal.send_mail(mail)
            return mail.send()
        except Exception:
            logger.warning(f"Send mail error - attempt {tries}")
            tries += 1
            if tries < SEND_MAIL_RETRIES:
                continue
            return logger.error(
                "Error sending mail. The user did not receive an error.\n"
                + traceback.format_exc()
                + f"\n\nMail content:\n\n{mail.body}"
            )


def dispatch_form_mail(
        to_address=None,
        reply_to=None,
        subject=None,
        text=None,
        html=None):
    """Send mail to support inbox.

    This should probably be sent to a worker thread but the SMTP server
    responds very quickly in production.
    """
    recipient = to_address or settings.EMAIL_TO_ADDRESS
    reply_to_value = [reply_to] if reply_to else None
    logger.info(f"Sending mail to {recipient}")
    email = EmailMultiAlternatives(
        subject,
        text,
        settings.EMAIL_FROM_ADDRESS,
        [recipient],
        reply_to=reply_to_value,
    )
    if html:
        email.attach_alternative(html, "text/html")
    retry_send_mail(email)


def user_success_mail(name, email, resource):
    """Dispatch access request success email to user."""
    subject = f"Access to {resource} granted"
    template = 'home/requests/mail/access-user-success'
    context = {
        'name': name,
        'resource_name': resource,
        'hostname': settings.HOSTNAME,
    }
    text = render_to_string(
        f'{template}.txt',
        context,
    )
    html = render_to_string(
        f'{template}.html',
        context,
    )
    mail = EmailMultiAlternatives(
        subject,
        text,
        settings.EMAIL_FROM_ADDRESS,
        [email],
    )
    mail.attach_alternative(html, "text/html")
    retry_send_mail(mail)


class OtherFieldFormMixin:
    """Handle validation/cleaning of 'other' fields.

    TODO: this should really be replaced with a custom Django field

    The inheriting class must define cls.OTHER_FIELDS as a tuple of field names
    for which a "field_other" field is expected. This field will be populated
    with the value of "other" if str(value) == "0".

    Typically this is involves an "Other" radiobuttom with a value of "0".
    """

    def __init__(self, *args, **kwargs):
        """Assert required other fields."""
        super().__init__(*args, **kwargs)
        for field in self.OTHER_FIELDS:
            if f'{field}_other' not in self.fields:
                raise AttributeError(
                    f"Expected field '{field}_other' not found in form."
                    " Fields declared as OTHER_FIELDS must be accompanied by"
                    " an '_other' field to provide the 'other' value."
                )

    def clean(self):
        data = self.cleaned_data
        for field in self.OTHER_FIELDS:
            field_value = data.get(field)
            if str(field_value) == '0':
                # User selected the 'other' field and typed a value
                other_value = data.get(f'{field}_other')
                logger.info(f"field_value: {field_value}")
                logger.info(f"other_value: {other_value}")
                if not other_value:
                    if self.fields[field].required:
                        self.add_error(
                            field,
                            ValidationError('This field is required'))
                        continue
                if type(other_value) == str:
                    data[field] = 'Other - ' + other_value
                else:
                    data[field] = other_value
        return data


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


class QuotaRequestForm(OtherFieldFormMixin, forms.Form):
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

    OTHER_FIELDS = ('disk_tb',)

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

    def dispatch(self, subject=None):
        """Dispatch content via the FreshDesk API."""
        data = self.cleaned_data
        dispatch_form_mail(
            reply_to=data['email'],
            subject=subject or "Galaxy Australia Support request",
            text=(
                f"Name: {data['name']}\n"
                f"Email: {data['email']}\n\n"
                + data['message']
            )
        )


class BaseAccessRequestForm(forms.Form):
    """Abstract form for requesting access to a resource.

    Handles auto Galaxy group assignment and dispatches emails to admins and
    users to notify them of the outcome.
    """

    AUTO_ACTION = False       # Some forms can be auto-actioned by GMS
    AUTO_ASSIGN_GROUP = True  # By default, assign user to the Galaxy group
    RESOURCE_NAME = None
    OTHER_FIELDS = []
    MAIL_SUCCESS_MESSAGE = (
        "This request has been actioned by Galaxy Media Site - no action is"
        " necessary but this request should be kept for reporting purposes."
    )
    MAIL_FAILED_MESSAGE = (
        "This request could not be actioned by Galaxy Media Site - please"
        " follow up on this request manually."
    )

    def clean_email(self):
        """Validate email address."""
        email = self.cleaned_data['email']
        if not is_institution_email(email):
            raise ValidationError(
                (
                    'Sorry, this is not a recognised Australian institution'
                    ' email address.'
                ),
                field="email",
            )
        return email

    def action(self, request, resource):
        error = None
        actioned = False
        email = self.cleaned_data['email']
        try:
            is_registered_email = galaxy.is_registered_email(email)
        except Exception as exc:
            logger.error(
                f"Error calling galaxy.is_registered_email():\n"
                f"{exc[:1000]}\n")
            error = (
                "Galaxy connection refused (could not check account"
                " status)."
            )
            # Admins will have to action this manually
            actioned = self.dispatch(exception=error)

        if is_registered_email:
            if self.AUTO_ASSIGN_GROUP:
                galaxy_group = resource
                logger.info(
                    f"Adding user {email} to Galaxy group {galaxy_group}")
                try:
                    galaxy.add_user_to_group(
                        self.cleaned_data['email'],
                        galaxy_group)
                except Exception as exc:
                    logger.error(
                        f"Error assigning user to Galaxy group:\n{exc}\n"
                        "This error was not fatal and the user's request"
                        " has been passed to the support email.")
                    error = exc
            logger.info(
                f"Dispatching {resource} request for email {email}")
            actioned = self.dispatch(exception=error)
        else:
            logger.info(f"Dispatching {resource} warning to {email}")
            self.dispatch_warning(request)

        return actioned

    def dispatch(self, exception=None, notify_user_success=True):
        """Dispatch form content as email.

        Returns "actioned" as a boolean.
        """
        subject = (
            f"ERROR actioning {self.RESOURCE_NAME} request on Galaxy Australia"
            if exception else
            f"Approved {self.RESOURCE_NAME} request on Galaxy Australia"
        )
        template = 'home/requests/mail/access-request'
        context = {
            'data': {
                field.name: {
                    'label': field.label,
                    'value': self.cleaned_data[field.name],
                }
                for field in self
                if not (
                    field.name.endswith("_other")
                    and field.name[:-6] in self.OTHER_FIELDS
                )
            },
            'resource_name': self.RESOURCE_NAME,
            'exception': exception,
            'success_message': self.MAIL_SUCCESS_MESSAGE,
            'failed_message': self.MAIL_FAILED_MESSAGE,
        }
        reply_to = None if self.AUTO_ACTION else self.cleaned_data['email']
        dispatch_form_mail(
            reply_to=reply_to,
            subject=subject,
            text=render_to_string(f'{template}.txt', context),
            html=render_to_string(f'{template}.html', context),
        )
        if not exception and notify_user_success:
            user_success_mail(
                self.cleaned_data['name'],
                self.cleaned_data['email'],
                self.RESOURCE_NAME,
            )
        actioned = not exception and self.AUTO_ACTION
        return actioned

    def dispatch_warning(self, request):
        """Dispatch warning email to let user know their email is invalid."""
        template = 'home/requests/mail/invalid-institutional-email'
        dispatch_form_mail(
            to_address=self.cleaned_data['email'],
            subject=f"Access to {self.RESOURCE_NAME} could not be granted",
            text=render_to_string(f'{template}.txt', {'form': self}),
            html=render_to_string(f'{template}.html', {
                'form': self,
                'hostname': settings.HOSTNAME,
                'scheme': request.scheme,
            }),
        )


class AlphafoldRequestForm(BaseAccessRequestForm):
    """Form to request AlphaFold access."""

    RESOURCE_NAME = 'AlphaFold'
    AUTO_ACTION = True

    name = forms.CharField()
    email = forms.EmailField(validators=[validators.institutional_email])
    institution = forms.CharField()
    species = forms.CharField(required=False)
    domain = forms.CharField(required=False, label="Domain of study")
    proteins = forms.CharField(required=False, label="Target proteins")
    size_aa = forms.IntegerField(required=False, label="Size (AA)")
    count_aa = forms.IntegerField(required=False, label="Total count (AA)")


class FgeneshRequestForm(BaseAccessRequestForm):
    """Form to request AlphaFold access."""

    RESOURCE_NAME = 'FGENESH++'
    MAIL_SUCCESS_MESSAGE = (
        "This request has been actioned by Galaxy Media Site and the user has"
        " been assigned to the 'fgenesh' group on Galaxy AU. An admin should"
        "  ensure that the required matrices are installed before notifying"
        " the user that the service is ready for use."
    )

    name = forms.CharField()
    email = forms.EmailField(validators=[validators.institutional_email])
    institution = forms.CharField()
    agree_terms = forms.BooleanField()
    agree_acknowledge = forms.BooleanField()
    research_description = forms.CharField(max_length=200, required=False)
    research_topics = forms.CharField(max_length=200, required=False)
    matrices = forms.MultipleChoiceField(choices=genematrix_tree.as_choices())

    def render_matrix_field(self):
        return genematrix_tree.as_ul()

    def dispatch(self, exception=None, notify_user_success=False):
        """Dispatch form without notifying user by default."""
        super().dispatch(
            exception=exception,
            notify_user_success=notify_user_success,
        )
        return False


class CellRangerRequestForm(BaseAccessRequestForm):
    """Form to request AlphaFold access."""

    RESOURCE_NAME = 'CellRanger'
    AUTO_ACTION = True

    name = forms.CharField()
    email = forms.EmailField(validators=[validators.institutional_email])
    institution = forms.CharField()


ACCESS_FORMS = {
    'alphafold': AlphafoldRequestForm,
    'fgenesh': FgeneshRequestForm,
    'cellranger': CellRangerRequestForm,
}
