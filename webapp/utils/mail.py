"""Custom mail handler for authenticating with Postal server."""

import smtplib
from django.conf import settings


def send_smtp_mail(email):
    """Dispatch mail with SMTP.

    This is only used for sending emails with specific headers (to satisfy the
    fussy Postal server).
    """
    try:
        # Create connection
        server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        server.ehlo(name="usegalaxy.org.au")
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

        if email.alternatives:
            body = email.alternatives[0][0]
            content_type = email.alternatives[0][1]
        else:
            body = email.body
            content_type = 'text/plain'
        data = (
            f'Content-Type: {content_type}; charset="us-ascii\n'
            'MIME-Version: 1.0\n'
            'Content-Transfer-Encoding: 7bit\n'
            f'From: {email.from_email}\n'
            f'To: {email.to[0]}\n'
            f'Subject: {email.subject}\n\n'
            + body
        )
        server.sendmail(
            settings.EMAIL_FROM_ADDRESS,
            email.to[0],
            data,
        )
    finally:
        server.quit()
