# Sending bulk email

**IMPORTANT**: this should be run on the GMS server only. If you REALLY have
to run this locally, make sure that you copy the `RECIPIENTS_MASTER_CSV` file
from the GMS server. After running, make sure that you update the
`RECIPIENTS_MASTER_CSV` file on the GMS server, so that GMS can look up the
hash table to unsubscribe users.

Intended recipients should be defined in the `RECIPIENTS_CSV` file.
Unsubscribed users are listed in files from various sources in the
`unsubscribed/` dir. These are manually updated from SMTP2GO correspondence,
and they *can* be deleted after `bulk_email.py --commit`, because the master
CSV will be updated with these records, and that will be persisted into future
runs.

An unsubscribe link is provided in the email footer, which points to a GMS
endpoint where the given email hash will be looked up in the
`RECIPIENTS_MASTER_CSV` hash table and a record added to the
'excluded_by' column.

Be **VERY CAREFUL** running this script - any mistakes will of course be echoed
to thousands of Galaxy AU users.

1. Edit `bulk_mail.py` to set `SUBJECT` to the email subject line.
1. Update `templates/body.*` files with your email content. It is recommended
to copy old templates to another file name so they can be re-used in future.
1. Update the `users.csv` file (you can create this file on the Galaxy AU web
server with `export_users_csv.sh`).
1. Ensure that `unsubscribed/*` lists are updated.

N.B. When running with `--commit`, be sure to run with `nohup` and expect
~1hr per 1000 emails sent. Collect the output carefully - if something goes
wrong you can pick up from the last attempted email.


## Files overview

- `bulk_mail.py`: this is the script used for test and real bulk mail runs
- `export_users_csv.sh`: SQL query to create the users.csv file
- `users.csv`: recipients will be read from this file
- `recipient_records.csv`: the master recipient list, containing a hash table
and exclusion (e.g. unsubscribed, bounced) status. This is created from either
a `--commit` or `--test-recipients` run of the `bulk_email.py` script.
- `unsubscribed/*.txt`: these lists come from SMTP2GO and list hard-bounced and
'reported us as spam' emails
- `templates/body.*`: these templates contain the email body in txt and HTML
and should be editted before sending.


## Testing the system

1. Create a recipient record file, if you don't have one already:
    ```sh
    python scripts/mail/bulk_mail.py --test-recipients

    # Rename to real master list file name so that GMS can cross-reference
    # against it. WARNING: don't do this if you have a real
    # recipient_records.csv in this directory. It will be deleted!

    if [ ! -f recipient_records.csv ]; then
        mv test_recipient_records.csv recipient_records.csv
    fi
    ```
1. Send a few emails to the mailtrap:
    ```sh
    python scripts/mail/bulk_mail.py --test
    ```
1. Run the media site locally with `python manage.py runserver`
1. Go to the mailtrap and copy the "unsubscribe" link in one of them. Replace
the `schema://hostname` with that of your local server
(probably `127.0.0.1:8000`) and paste into the browser.
1. You should see an "Unsubscribe success" page from the local server.
1. Check the `RECIPIENTS_MASTER_CSV` file - an entry should have been made in
the 'excluded_by' column for that email address.
1. Run `bulk_mail.py --test` again. Check that the unsubscribed
email from above has indeed been excluded.


## Sending mail for real

Please be careful.

- Make sure exclude lists in `unsubscribed/` have been updated from SMTP2GO's correspondence.
- Make sure the `RECIPIENTS_MASTER_CSV` file has been copied from the GMS server
if you aren't running there (recommended).
- Do some test runs to make sure it's all good:
    ```sh
    # check mail content is OK in the configured mailtrap.io account
    python scripts/mail/bulk_mail.py --test

    # check the recipient list looks good
    python scripts/mail/bulk_mail.py --test-recipients

    # send to TEST_RECIPIENTS with prod mail server
    python scripts/mail/bulk_mail.py --test-server
    ```
- Send it (this may take a good few hours, prepare to leave overnight)
    ```sh
    nohup python scripts/mail/bulk_mail.py --commit > sending.out 2> sending.err &
    ```
- If you did not run on the GMS server (cowboy) then make sure you copy the
`RECIPIENTS_MASTER_CSV` file back to the server so it can handle the
'unsubscribe' requests (this file contains the hash table required to look up
email addresses, and unsubscribe status is recorded there).
