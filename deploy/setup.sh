# Config production server setup

# Drop into ./deploy if user called from root dir
[[ -d deploy ]] && [[ -d webapp ]] && cd deploy

if [[ $1 = '--clean' ]]; then

    if [[ -f ../.env ]]; then
        source ../.env
    fi

    echo "Removing server configuration from the system."
    echo "Press <ENTER> to continue or CTRL+C to cancel."
    read abc
    echo "Removing server conf..."
    sudo systemctl stop webapp.socket
    sudo systemctl stop webapp.service
    sudo systemctl disable webapp.socket
    sudo systemctl disable webapp.service
    sudo rm /etc/systemd/system/webapp.socket
    sudo rm /etc/systemd/system/webapp.service
    sudo rm /etc/nginx/sites-available/webapp.conf /etc/nginx/sites-enabled/webapp
    sudo rm -r /srv/sites/webapp
    sudo systemctl daemon-reload
    echo "Done"

    echo "Remove Postgres user/database? [y/n]"
    read rmdb
    if [[ $rmdb = 'y' ]]; then
        echo "Removing database configuration..."
        sudo -u postgres psql -c "DROP DATABASE $DB_NAME;"
        sudo -u postgres psql -c "DROP USER $DB_USER;"
    else
        echo "Leaving database configuation"
    fi

    exit 0;
fi

set -e

# Webserver config
cat << EOI

~~~~~~~~~~ GALAXY MEDIA SITE ~~~~~~~~~~~~

Author: Cameron Hyde, QCIF Bioinformatics

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

** This software has been developed and tested on Ubuntu 20.04 LTS **
** We do not recommend installation on any other operating system **

This script will install and set up Galaxy Media Site on the current machine.
Please make sure that you have set the required variables in a .env file in the
project root (copy .env.sample).

  - set DJANGO_SECRET_KEY and DB_PASSWORD to something secure (no hash chars)
  - set HOSTNAME to the domain name that the site will be hosted under
    (e.g. example.com)

To remove system configuration after install, run with --clean flag

Press <ENTER> to continue or CTRL-C to cancel.
EOI
read abc

if [[ ! -f ../.env ]]; then
    printf "\n.env not found in the root directory.\nPlease create an \
environment file as described above.\n"
    exit 1;
fi

source ../.env

cat << EOI

~~~~~~~ SSL configuration ~~~~~~~

If you are the owner of the domain name "$HOSTNAME", you can
configure SSL for secure serving over HTTPS. This is required for production
deployments, for security and technical reasons! You cannot display this site
within a Galaxy instance if serving without SSL. In order to configure SSL
successfully, you must set a DNS "A" record with your DNS provider (e.g.
CloudFlare, GoDaddy) which points the hostname to the IP address of this
machine ($(curl --no-progress-meter icanhazip.com)).

Configure SSL certificates with certbot (requires user input)? [y/n]
EOI

while true; do
    read ssl
    case $ssl in
        y|n)        break;;
    esac
    printf "\nOption not recognised.\n"
    echo "Run certbot to configure SSL certificates? [y/n]"
done

echo ""
echo "Installing system dependancies..."
sudo apt-get update \
&& sudo apt-get install -y --no-install-recommends \
    python3.8 \
    python3-pip \
    postgresql postgresql-client \
    nginx \
    certbot python3-certbot-nginx

export PATH=/home/$USER/.local/bin:$PATH
echo "export PATH=/home/$USER/.local/bin:$PATH" >> /home/$USER/.bashrc

python3.8 -m pip install --no-cache-dir --upgrade pip
python3.8 -m pip install --no-cache-dir virtualenv

echo ""
echo "Creating virtual environment..."
python3.8 -m virtualenv .venv
source .venv/bin/activate
python3.8 -m pip install --no-cache-dir -r ../requirements.txt

echo ""
echo "Configuring webserver with Nginx and Gunicorn..."
sed "s/{{ HOSTNAME }}/$HOSTNAME/" nginx.conf.tmpl > nginx.conf
sed "s|{{ PWD }}|$PWD|" webapp.service.tmpl > webapp.service
sudo ln -s $PWD/webapp.service /etc/systemd/system/webapp.service
sudo ln -s $PWD/webapp.socket /etc/systemd/system/webapp.socket
sudo ln -s $PWD/nginx.conf /etc/nginx/sites-available/webapp.conf
sudo ln -s /etc/nginx/sites-available/webapp.conf /etc/nginx/sites-enabled/webapp
sudo mkdir -p /srv/sites
sudo ln -s "$(dirname $PWD)/webapp" /srv/sites/webapp
sudo chown ubuntu:ubuntu /srv/sites/webapp

echo ""
if [[ $ssl = 'y' ]]; then
    echo "Configuring SSL with Certbot..."
    sudo certbot --nginx -d $HOSTNAME
elif [[ $ssl = 'n' ]]; then
    echo "Skipping SSL..."
fi

# Set up database
echo ""
echo "Configuring database..."
sudo -u postgres createuser $DB_USER
sudo -u postgres createdb $DB_NAME
sudo -u postgres psql << SQL
ALTER USER $DB_NAME WITH PASSWORD '$DB_PASSWORD';
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
SQL

# Start services
echo ""
echo "Reloading system services..."
sudo service nginx restart
sudo service postgresql restart
sudo systemctl daemon-reload
sudo systemctl enable webapp.socket
sudo systemctl enable webapp.service
sudo service webapp start

# Migrate database
echo ""
echo "Migrating database schema..."
python3.8 ../webapp/manage.py migrate

# Configure default user
echo ""
echo "~~~~~ Create superuser login ~~~~~"
echo ""
echo "Please enter sensible superuser login credentials for this site."
echo "N.B. users can be further managed from within the admin interface,"
echo "once the application has launched. These login credentials will be"
echo "required to access the admin interface, so keep them safe!"
echo ""
python3.8 ../webapp/manage.py createsuperuser

# Static file setup
python3.8 ../webapp/manage.py collectstatic --noinput

printf "\nSetup complete!\n\n"
case $ssl in
    "y" )   echo "Now serving at https://$HOSTNAME";;
    "n" )   echo "Now serving at http://$HOSTNAME";;
esac

cat << EOI

Some management tips:

- Test gunicorn wsgi server:
  curl --unix-sock /run/webapp.sock http://localhost

- Check systemd services status:
  sudo service nginx status
  sudo service webapp status
  sudo service postgresql status

- Check socket status:
  sudo systemctl status webapp.socket

EOI
