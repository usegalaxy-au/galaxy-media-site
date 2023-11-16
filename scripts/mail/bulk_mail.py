#!/usr/bin/env python

"""Send bulk email to Galaxy Australia users.

Users are defined in the ``RECIPIENTS_CSV`` file.
Unsubscribed users are listed in files from various sources in the
unsubscribed/ dir. These are manually updated from SMTP2GO correspondence, and
automatically from the GMS unsubscribe list.

This list is cross-referenced when sending emails. An
unsubscribe link is provided in the email footer.

Be VERY CAREFUL running this script, as mistakes will obviously be distributed
to thousands of Galaxy AU users!

- Set ``SUBJECT``
- Update ``BODY_TEXT_TEMPLATE`` and ``BODY_HTML_TEMPLATE``
- Update ``RECIPIENTS_CSV`` file (created with ``export_users_csv.sh``)
- Ensure that lists in ``unsubscribed/`` are updated.

When running with ``--commit``, be sure to run with ``nohup`` and expect ~1hr
per 1000 emails sent.
"""

import argparse
import chardet
import smtplib
import os
import sys
import time
import pandas as pd
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
RECIPIENTS_MASTER_CSV = Path(__file__).parent / 'recipient_records.csv'
BODY_TEXT_TEMPLATE = Path(__file__).parent / 'templates/body.txt'
BODY_HTML_TEMPLATE = Path(__file__).parent / 'templates/body.html'
UNSUBSCRIBED_EMAIL_FILES = [
    # This file is written to by GMS:
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

    if args.test:
        return send_test_mail()

    if args.test_server:
        return send_bulk_mail(
            SMTP_HOSTNAME,
            SMTP_PORT,
            SMTP_USERNAME,
            SMTP_PASSWORD,
            test=True)

    if args.test_recipients:
        return test_recipient_list()

    if args.commit:
        return send_bulk_mail(
            SMTP_HOSTNAME,
            SMTP_PORT,
            SMTP_USERNAME,
            SMTP_PASSWORD,
            write=True,
        )

    print("No action specified. Please see --help for options.")


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
        '--test-recipients',
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


def send_bulk_mail(
    hostname,
    port,
    username,
    password,
    limit=None,
    test=False,
    write=False,
):
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
    recipients = build_recipient_df(test=test, limit=limit, write=write)
    n_recipients = len(recipients)

    if '-y' not in sys.argv:
        input(f"Sending mail to {n_recipients} recipients.\n\n"
              "Press enter to continue...\n\n> ")

    server = smtp_connect(hostname, port, username, password)

    for ix, recipient in recipients.iterrows():
        email = recipient['email']
        if '@' not in email or '.' not in email:
            print(f"Skipping recipient with invalid email: {email}",
                  file=sys.stderr)
            continue

        msg = build_smtp_body(recipient)

        print(f"Sending mail to recipient {ix + 1}/{n_recipients} {email}...",
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


def test_recipient_list():
    """Test parsing of recipient and excluded lists."""
    recipients = build_recipient_df(write=True, test=True)
    print(f'Collected {len(recipients)} recipients:')
    i = 0
    for _, recipient in recipients.iterrows():
        i += 1
        print(recipient['username'].ljust(40) + recipient['email'])
        if i > 5:
            print('...')
            break
    print()


def build_recipient_df(test=False, limit=None, write=False):
    """Build dataframe of recipients from csv and exclude lists.

    If write=True, update the master recipient CSV with new recipients and
    exclusion records.
    """
    print("Building recipient list...")
    recipients = (
        pd.DataFrame.from_records(TEST_RECIPIENTS)
        if test and not write else
        read_recipients(limit=limit)
    )
    exclude_list = read_exclude_email_list()
    exclude_list_flat = read_exclude_email_list(flat=True)
    if write:
        recipient_table = write_recipient_list(
            recipients, exclude_list, test=test)
        filtered_recipients = recipient_table[
            recipient_table['excluded_by'].isna()
        ]
    else:
        filtered_recipients = recipients[
            ~recipients['email'].isin(exclude_list_flat)
        ]
    print(f"\nExcluded {len(recipients) - len(filtered_recipients)}"
          f"/{len(recipients)} recipients")
    return filtered_recipients


def write_recipient_list(recipients, excluded, test=False):
    """Update the master recipient list for future reference.

    This sheet will contain all records for unsubscribed, bounced, spam and a
    hash table for email lookup that is user by GMS for unsubscribe requests.
    """
    csv_file = RECIPIENTS_MASTER_CSV
    if test:
        csv_file = csv_file.parent / f'test_{csv_file.name}'
    cols = ['username', 'email', 'hash', 'excluded_by']
    if csv_file.exists():
        df = pd.read_csv(csv_file)
    else:
        df = pd.DataFrame(columns=cols)

    # Add new recipients to master list
    df_r = recipients[['username', 'email']]
    df_new_recipients = df_r[~df_r['email'].isin(df['email'])]
    df_new_recipients['hash'] = df_new_recipients['email'].apply(hash_email)
    df_new = pd.concat([df, df_new_recipients])

    excluded_rows = []
    emails_not_found = []
    for src_filename, email_list in excluded.items():
        for email in email_list:
            username = None
            user_row = df_new[df_new['email'] == email]
            if len(user_row):
                username = user_row['username'].values[0]
            else:
                emails_not_found.append(f"{email} ({src_filename})")
                continue
            excluded_rows.append({
                'username': username,
                'email': email,
                'hash': None,
                'excluded_by': src_filename,
            })

    if emails_not_found:
        print(f"\nWARNING: {len(emails_not_found)} emails not found in "
              f"master recipient list. This is a no-op, but it should not"
              " happen because these emails originate from the master list."
              " Most likely this is because Galaxy AU dispatched emails to"
              " these users for some other reason:"
              )
        print(', '.join(emails_not_found))
    df_ex = pd.DataFrame.from_records(excluded_rows, columns=cols)

    # Update df rows matching excluded recipients
    for _, row in df_ex.iterrows():
        df_new.loc[
            df_new['email'] == row['email'], 'excluded_by'
        ] = row['excluded_by']

    df_new.to_csv(csv_file, index=False)

    return df_new


def hash_email(email):
    """Generate MD5 hash from email string."""
    return md5(email.encode()).hexdigest()


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
    print(f"Reading recipients from {RECIPIENTS_CSV}...")
    with open(RECIPIENTS_CSV, 'rb') as f:
        encoding = chardet.detect(f.read())['encoding']
    with open(RECIPIENTS_CSV, encoding=encoding) as f:
        recipients = pd.read_csv(f)
    if limit:
        recipients = recipients.head(limit)
    recipients['email'] = recipients['email'].str.lower()
    return recipients


def read_exclude_email_list(flat=False):
    """Combine emails to skip from unsubscribe/spam lists."""
    skip_emails = {}
    for path in UNSUBSCRIBED_EMAIL_FILES:
        print(f"Reading excluded recipients from {path.name}...")
        with open(path) as f:
            skip_emails[path.name] = [
                line.strip().lower()
                for line in f.readlines()
                if line.strip()
                and not line.startswith('#')
            ]

    if not flat:
        return skip_emails

    flattened = []
    for email_list in skip_emails.values():
        flattened += email_list

    return flattened


if __name__ == '__main__':
    test_recipient_list()
