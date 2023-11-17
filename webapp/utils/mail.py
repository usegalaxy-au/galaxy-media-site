"""Utilities for sending mail."""

import logging
import traceback
from django.conf import settings

from . import postal

SEND_MAIL_RETRIES = 3

logger = logging.getLogger(__name__)


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
