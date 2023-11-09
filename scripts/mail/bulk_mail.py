#!/usr/bin/env python

import chardet
import csv
import smtplib
import os
import sys
import time
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment
from pathlib import Path

engine = Environment()

load_dotenv(Path(__file__).parent.parent.parent / '.env')

SUBJECT = 'Galaxy Australia Satisfaction Survey 2023'
FROM_ADDRESS = 'galaxy-no-reply@usegalaxy.org.au'
SMTP_HOSTNAME = os.getenv('PROD_SMTP_HOSTNAME')
SMTP_PORT = os.getenv('PROD_SMTP_PORT')
SMTP_USERNAME = os.getenv('PROD_SMTP_USERNAME')
SMTP_PASSWORD = os.getenv('PROD_SMTP_PASSWORD')

SMTP_TEST_HOSTNAME = os.getenv('MAIL_HOSTNAME')
SMTP_TEST_PORT = os.getenv('MAIL_SMTP_PORT')
SMTP_TEST_USERNAME = os.getenv('MAIL_SMTP_USERNAME')
SMTP_TEST_PASSWORD = os.getenv('MAIL_SMTP_PASSWORD')

# RECIPIENTS_CSV = Path(__file__).parent / 'users_2023.csv'
# RECIPIENTS_CSV = Path(__file__).parent / 'users_2023_2.csv'
# RECIPIENTS_CSV = Path(__file__).parent / 'users_2023_3.csv'
RECIPIENTS_CSV = Path(__file__).parent / 'users_2023_4.csv'
BODY_TEXT_TEMPLATE = Path(__file__).parent / 'templates/body.txt'
BODY_HTML_TEMPLATE = Path(__file__).parent / 'templates/body.html'

MAX_MESSAGES_PER_CONNECTION = 2000

TEST_RECIPIENTS = [
    {
        'email': 'c.hyde@qcif.edu.au',
        'username': 'chyde',
    },
    {
        'email': 'chyde1@usc.edu.au',
        'username': 'chyde_usc',
    },
]


def send_test_mail():
    """Send bulk mail with test SMTP server."""
    send_bulk_mail(
        SMTP_TEST_HOSTNAME,
        SMTP_TEST_PORT,
        SMTP_TEST_USERNAME,
        SMTP_TEST_PASSWORD,
        limit=5,
    )


def send_bulk_mail(hostname, port, username, password, limit=None, test=False):
    """Send SMTP mail to recipient list."""
    k = 0  # messages in connection
    recipients = (
        TEST_RECIPIENTS
        if test else
        read_recipients(limit=limit)
    )
    n_recipients = len(recipients)

    if '-y' not in sys.argv:
        input(f"Sending mail to {len(recipients)} recipients.\n\n"
              "Press enter to continue...\n\n> ")

    server = smtp_connect(hostname, port, username, password)

    for i, recipient in enumerate(recipients):
        email = recipient['email']
        if '@' not in email or '.' not in email:
            print(f"Skipping recipient with invalid email: {email}",
                  file=sys.stderr)
            continue

        msg = MIMEMultipart('alternative')
        msg['Subject'] = SUBJECT
        msg['From'] = FROM_ADDRESS
        msg['To'] = email

        with open(BODY_TEXT_TEMPLATE) as f:
            text_template = engine.from_string(f.read())
            body_text = text_template.render(recipient=recipient)
        with open(BODY_HTML_TEMPLATE) as f:
            html_template = engine.from_string(f.read())
            body_html = html_template.render(recipient=recipient)

        msg.attach(MIMEText(body_text, 'plain'))
        msg.attach(MIMEText(body_html, 'html'))

        print(f"Sending mail to recipient {i + 1}/{n_recipients} {email}...",
              flush=True)
        server.sendmail(FROM_ADDRESS, email, msg.as_string())
        k += 1
        print("Mail sent successfully")

        if k >= MAX_MESSAGES_PER_CONNECTION:
            print(f"Max messages per connection reached: ({k})")
            print("Closing connection...")
            server.quit()
            time.sleep(1)
            print("Reopening connection...")
            server = smtp_connect(hostname, port, username, password)
            k = 0

    print("\nDone")

    server.quit()


def smtp_connect(hostname, port, username, password):
    """Start an SMTP connection with the given credentials."""
    server = smtplib.SMTP(hostname, port)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(username, password)
    return server


def read_recipients(limit=None):
    """Read recipients from csv to dictionary."""
    print("\nReading recipients list...\n")
    recipients = []
    with open(RECIPIENTS_CSV, 'rb') as f:
        encoding = chardet.detect(f.read())['encoding']
    with open(RECIPIENTS_CSV, newline='', encoding=encoding) as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if limit and i >= limit:
                break
            recipients.append(row)
    return recipients


def print_peek_recipients():
    """List recipients from csv."""
    recipients = read_recipients()
    print(f"Read {len(recipients)} recipients from {RECIPIENTS_CSV}")
    for recipient in recipients[:5]:
        print(recipient['username'].ljust(40) + recipient['email'])


if __name__ == '__main__':
    print("\nRead mail credentials:")
    print(f"SMTP_HOSTNAME: {SMTP_HOSTNAME}")
    print(f"SMTP_PORT: {SMTP_PORT}")
    print(f"SMTP_USERNAME: {SMTP_USERNAME}")
    print(f"SMTP_PASSWORD: {SMTP_PASSWORD}\n")

    # print_peek_recipients()

    # send_test_mail()

    # send_bulk_mail(
    #     SMTP_HOSTNAME,
    #     SMTP_PORT,
    #     SMTP_USERNAME,
    #     SMTP_PASSWORD,
    #     test=True)

    send_bulk_mail(SMTP_HOSTNAME, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD)
