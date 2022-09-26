"""Custom mail handler for authenticating with Postal server."""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.conf import settings

# It doesn't matter what this is, as long as it doesn't occur in the email body
CONTENT_BOUNDARY = 'content-type-boundary'


def send_mail(email):
    """Dispatch mail with SMTP.

    This is only used for sending emails with specific headers (to satisfy the
    fussy Postal server).
    """
    try:
        # Create connection
        server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        server.ehlo(name="usegalaxy.org.au")
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

        # Build multipart email content
        m = MIMEMultipart('alternative')
        m['To'] = email.to[0]
        m['From'] = email.from_email
        m['Subject'] = email.subject
        if email.reply_to:
            m['Reply to'] = email.reply_to[0]

        text = MIMEText(email.body, 'plain')
        m.attach(text)

        for content in email.alternatives:
            m.attach(MIMEText(
                content[0],                       # content
                content[1].replace('text/', ''),  # type
            ))

        server.send_message(m)

    finally:
        server.quit()
