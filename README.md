# Galaxy Media Site

A content site for a Galaxy instance, built with Django.

---

## What it does

This web application is designed to host content related to a [Galaxy](https://galaxyproject.org/) instance. It is lightweight, easy to install and maintain, and provides interfaces for publishing:

- Events
- News items (including automated tool updates)
- Team members
- Homepage alerts (Notices)

The site also hosts some static pages including:

- Terms of service
- Data policy
- About page

If you fork the repository, these templates can be updated with content relevant to your Galaxy instance.

The homepage is designed to be displayed as your Galaxy instance welcome page. Just create a `welcome.html` file with an `iframe` that points to https://mysite.com/landing to get a landing page without the navbar.

The site is designed to be fully navigable from within your Galaxy instance, with the Navbar being nested under the Galaxy navbar:



---

## Installation

If you are setting this up for production, create a DNS record for your domain name before running the setup script - this should be an A record pointing to the IP address of the host machine.

```bash
# This site has been developed and tested on Ubuntu 20.04 LTS.
# Other operating systems may require manual installation.
# The application is installed on a Nginx-Gunicorn-Postgres stack
# and is not containerized. We recommend installation in a fresh
# virtual machine instance.

cd <my-projects-directory>
git clone https://github.com/neoformit/galaxy-content-site.git

cd galaxy-content-site

# Follow prompts
./deploy/setup.sh

# Check operation with Django local serve
# Will provide feedback on any issues detected
source deploy/.venv/bin/activate
python webapp/manage.py runserver
```

---

## Administration

Visit `/admin/login` and log in with a staff user account. If you don't have one, you can create one with the Django CLI:

```bash
source deploy/.venv/bin/activate

# Follow prompts
python webapp/manage.py createsuperuser
```

---

## Migration

If required, you can migrate the application between servers.

> N.B. if the database user name has changed, you will have to dump the database with the `--no-owner` flag and create privileges for the new owner manually in a `psql` shell.

1. Get a db dump on the old machine:

  `sudo -u postgres pg_dump <dbname> > gm.sql`

2. Run `deploy/setup.sh` on the new server (N.B superuser will be overwritten by the following steps)

3. Drop and recreate the new database
  ```
  sudo -u postgres psql -c "DROP DATABASE <dbname>"
  sudo -u postgres psql -c "CREATE DATABASE <dbname>"
  sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE <dbname> TO <user>"
  ```

4. Load the db dump

  `sudo -u postgres psql -d <dbname> < gm.sql`

5. Check out the new site, the content should be there.

6. Images/media must be migrated separately. `tar` the `webapp/webapp/media` directory and `sftp` to the new server. Untar in the same location on the new server and your media content should become accessible.

7. If you are using a Jenkins task for automated news posts, you will need to update the Jenkins config if the hostname has changed.
