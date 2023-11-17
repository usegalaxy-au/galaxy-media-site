"""Functions for unsubscribing user from mail."""

import logging
import traceback
import pandas as pd
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .mail import retry_send_mail

logger = logging.getLogger('django')


def add(user_hash):
    """Add user email to unsubscribe list."""
    try:
        records = pd.read_csv(settings.RECIPIENT_MASTER_CSV)
        records.loc[
            records['hash'] == user_hash, 'excluded_by'
        ] = 'unsubscribed'
        records.to_csv(settings.RECIPIENT_MASTER_CSV)
        user_email = records.loc[
            records['hash'] == user_hash, 'email'
        ].values[0]
        report_user_unsubscribe(user_email)
    except Exception:
        logger.error(
            f"Failed to unsubscribe user with email_hash={user_hash}\n"
            + traceback.format_exc())


def report_user_unsubscribe(user_email):
    """Send email to admin reporting user unsubscribe."""
    subject = 'User unsubscribed from Galaxy Australia mailing list'
    text = render_to_string(
        'mail/report_unsubscribe.txt',
        {'user_email': user_email}
    )
    email = EmailMultiAlternatives(
        subject=subject,
        body=text,
        from_email=settings.EMAIL_FROM_ADDRESS,
        to=[settings.EMAIL_TO_ADDRESS],
    )
    retry_send_mail(email)
