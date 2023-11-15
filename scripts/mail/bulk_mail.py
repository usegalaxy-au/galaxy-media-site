#!/usr/bin/env python

"""Send bulk email to Galaxy Australia users.

Users are defined in the ``RECIPIENTS_CSV`` file.
Unsubscribed users are listed in `unsubscribed.txt` with an md5 hash of
their email address. This list is cross-referenced when sending emails. An
unsubscribe link is provided in the email footer.

Be VERY CAREFUL running this script, as mistakes will obviously be distributed
to thousands of Galaxy AU users!

- Set ``SUBJECT``
- Update ``BODY_TEXT_TEMPLATE`` and ``BODY_HTML_TEMPLATE``
- Update ``RECIPIENTS_CSV`` file (see ``export_users_csv.sh``)
- Ensure that lists in ``unsubscribe/`` are updated.

When running with ``--commit``, be sure to run with ``nohup`` and expect ~1hr
per 1000 emails sent.
"""

import argparse
import chardet
import csv
import smtplib
import os
import sys
import time
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from hashlib import md5
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

RECIPIENTS_CSV = Path(__file__).parent / 'users_2023.csv'
BODY_TEXT_TEMPLATE = Path(__file__).parent / 'templates/body.txt'
BODY_HTML_TEMPLATE = Path(__file__).parent / 'templates/body.html'
UNSUBSCRIBED_HASH_FILE = Path(__file__).parent / 'unsubscribed/hash.txt'
UNSUBSCRIBED_EMAIL_FILES = [
    Path(__file__).parent / 'unsubscribed/emails.txt',
    # These files are sent to us from SMTP2GO:
    Path(__file__).parent / 'unsubscribed/spam_emails.txt',
    Path(__file__).parent / 'unsubscribed/bounced_emails.txt',
]
UNSUBSCRIBE_URL = 'https://site.usegalaxy.org.au/unsubscribe'

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


def main():
    """Script entrypoint. Comment in/out these lines to test/commit."""
    args = parse_args()

    if args.dry:
        print_peek_recipients()
        sys.exit(0)

    if args.test:
        send_test_mail()

    if args.test_server:
        send_bulk_mail(
            SMTP_HOSTNAME,
            SMTP_PORT,
            SMTP_USERNAME,
            SMTP_PASSWORD,
            test=True)

    if args.commit:
        send_bulk_mail(
            SMTP_HOSTNAME, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD)


def parse_args():
    """Parse command line arguments to determine appropriate action."""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--test',
        action='store_true',
        help="Send test mail to recipients")
    parser.add_argument(
        '--test-server',
        action='store_true',
        help="Send mail with prod server to test recipients")
    parser.add_argument(
        '--dry',
        action='store_true',
        help="Show parsed recipients list peek and exit")
    parser.add_argument(
        '--commit',
        action='store_true',
        help="Confirm sending bulk mail to recipient list")
    return parser.parse_args()


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
    # Check SMTP vars are available:
    print("\nRead mail credentials:")
    for name, value in (
        ('SMTP hostname', hostname),
        ('SMTP port', port),
        ('SMTP username', username),
        ('SMTP password', password),
    ):
        if not value:
            raise Exception(
                f"Missing env variable for '{name}'. Please check .env file.")
        print(f"{name}: {value}")

    k = 0  # messages in connection
    recipients = build_recipient_list(test, limit)
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

        msg = build_smtp_body(recipient)

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


def build_recipient_list(test, limit):
    recipients = (
        TEST_RECIPIENTS
        if test else
        read_recipients(limit=limit)
    )
    exclude_list = read_exclude_email_list()
    exclude_hash_list = read_exclude_email_hash_list()
    return [
        r for r in recipients
        if r['email'] not in exclude_list
        and md5(r['email'].encode()).hexdigest() not in exclude_hash_list
    ]


def build_smtp_body(recipient):
    """Build multipart SMTP email from templates."""
    msg = MIMEMultipart('alternative')
    email = recipient['email']
    msg['Subject'] = SUBJECT
    msg['From'] = FROM_ADDRESS
    msg['To'] = email
    email_md5 = md5(email.encode()).hexdigest()
    unsubscribe_href = f"{UNSUBSCRIBE_URL}?id={email_md5}"
    with open(BODY_TEXT_TEMPLATE) as f:
        text_template = engine.from_string(f.read())
        body_text = text_template.render(
            recipient=recipient,
            unsubscribe_href=unsubscribe_href,
        )
    with open(BODY_HTML_TEMPLATE) as f:
        html_template = engine.from_string(f.read())
        body_html = html_template.render(
            recipient=recipient,
            unsubscribe_href=unsubscribe_href,
        )
    msg.attach(MIMEText(body_text, 'plain'))
    msg.attach(MIMEText(body_html, 'html'))

    return msg


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


def read_exclude_email_list():
    """Combine emails to skip from unsubscribe/spam lists."""
    skip_emails = []
    for path in UNSUBSCRIBED_EMAIL_FILES:
        with open(path) as f:
            skip_emails += [
                line.strip()
                for line in f.readlines()
                if line.strip()
                and not line.startswith('#')
            ]
    return skip_emails


def read_exclude_email_hash_list():
    """Read email hashes from unsibscribe hash file."""
    with open(UNSUBSCRIBED_HASH_FILE) as f:
        skip_hashes = [
            line.strip()
            for line in f.readlines()
            if line.strip()
            and not line.startswith('#')
        ]
    return skip_hashes


def print_peek_recipients():
    """List recipients from csv."""
    recipients = read_recipients()
    print(f"Read {len(recipients)} recipients from {RECIPIENTS_CSV}")
    for recipient in recipients[:5]:
        print(recipient['username'].ljust(40) + recipient['email'])


if __name__ == '__main__':
    main()
