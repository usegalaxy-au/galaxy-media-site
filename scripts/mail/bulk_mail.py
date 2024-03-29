#!/usr/bin/env python

"""Send bulk email to Galaxy Australia users.

IMPORTANT: this should be run on the GMS server only. If you REALLY have
to run this locally, make sure that you copy the ``RECIPIENTS_MASTER_CSV`` file
from the GMS server. After running, make sure that you update the
``RECIPIENTS_MASTER_CSV`` file on the GMS server, so that GMS can look up the
hash table to unsubscribe users.

Intended recipients should be defined in the ``RECIPIENTS_CSV`` file.
Unsubscribed users are listed in files from various sources in the
unsubscribed/ dir. These are manually updated from SMTP2GO correspondence.

An unsubscribe link is provided in the email footer, which points to a GMS
endpoint where the given email hash will be looked up in the
``RECIPIENTS_MASTER_CSV`` hash table and a record will be added to the
'excluded_by' column.

Be VERY CAREFUL running this script - any mistakes will of course be echoed
to thousands of Galaxy AU users.

1) Set ``SUBJECT``
2) Update ``BODY_TEXT_TEMPLATE`` and ``BODY_HTML_TEMPLATE``
3) Update ``RECIPIENTS_CSV`` file (created with ``export_users_csv.sh``)
4) Ensure that ``unsubscribed/*`` lists are updated.

N.B. When running with ``--commit``, be sure to run with ``nohup`` and expect
~1hr per 1000 emails sent. Collect the output carefully - if something goes
wrong you can pick up from the last attempted email.
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

RECIPIENTS_CSV = Path(__file__).parent / 'users.csv'
RECIPIENTS_MASTER_CSV = Path(__file__).parent / 'recipient_records.csv'
BODY_TEXT_TEMPLATE = Path(__file__).parent / 'templates/body.txt'
BODY_HTML_TEMPLATE = Path(__file__).parent / 'templates/body.html'
UNSUBSCRIBED_EMAIL_FILES = [
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
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--test',
        action='store_true',
        help="Send test mail to recipients with configured mailtrap.io server")
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
    if 'mailtrap' not in SMTP_TEST_HOSTNAME:
        raise ValueError(
            "SMTP_TEST_HOSTNAME must be set to a mailtrap.io hostname."
            " Please check MAIL_HOSTNAME value in .env file.")
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

    server = smtp_connect(hostname, port, username, password)

    for ix, recipient in recipients.iterrows():
        email = recipient['email']
        if '@' not in email or '.' not in email:
            print(f"Skipping recipient with invalid email: {email}",
                  file=sys.stderr)
            continue

        msg = build_smtp_body(recipient)

        print(f"Sending mail to recipient {ix}/{n_recipients} {email}...",
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
    recipient_table = write_recipient_table(
        recipients, exclude_list, test=test, write=write)
    filtered_recipients = recipient_table[
        recipient_table['excluded_by'].isna()
    ][
        recipient_table['email'].isin(recipients['email'])
    ]
    print(f"\nExcluded {len(recipients) - len(filtered_recipients)}"
          f"/{len(recipients)} recipients")
    return filtered_recipients


def write_recipient_table(recipients, excluded, test=False, write=True):
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

    if write:
        print(f"\nWriting {len(df_new)} recipients to {csv_file.name}...")
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
    print(f"Reading recipients from {RECIPIENTS_CSV.name}...")
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
    main()
