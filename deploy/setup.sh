# Config production server setup

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

Press <ENTER> to continue or CTRL-C to cancel.
EOI
read abc

if [[ ! -f ../.env ]]; then
    printf "\n.env not found in the root directory. Please create an \
environment file as described above."
    exit 1;
fi

source ../.env

printf "Configure SSL certificates with certbot (requires user input)? [y/n]\n"
while true; do
    read ssl
    case $ssl in
        y|n)        break;;
    esac
    printf "\nOption not recognised.\n"
    echo "Run certbot to configure SSL certificates? [y/n]"
done

echo "Installing system dependancies..."
apt-get update \
&& apt-get install -y --no-install-recommends \
    python3.8 \
    python3-pip \
    postgresql-client \
    nginx \
    certbot python3-certbot-nginx

python3.8 -m pip install --no-cache-dir --upgrade pip
python3.8 -m pip install --no-cache-dir -r requirements.txt

sed "s/{{ HOSTNAME }}/$HOSTNAME/" nginx.conf.tmpl > nginx.conf
ln -s gunicorn.service /etc/systemd/system/webapp.service
ln -s gunicorn.socket /etc/systemd/system/webapp.socket
ln -s nginx.conf /etc/nginx/sites-available/webapp.conf
ln -s /etc/nginx/sites-available/webapp.conf /etc/nginx/sites-enabled/webapp
rm /etc/nginx/sites-enabled/default

if [[ $ssl = 'y' ]]; then
    echo "Contiguring SSL with Certbot..."
    sudo certbot --nginx -d $HOSTNAME
elif [[ $ssl = 'n' ]]; then
    echo "Skipping SSL..."

# Set up database
echo "Configuring database"
su postgres
postgres createuser $DB_USER
postgres createdb $DB_NAME
psql <<SQL
ALTER USER $DB_NAME WITH PASSWORD $DB_PASSWORD;
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
SQL

# Start services
service nginx restart
service postgresql restart
systemctl enable webapp.socket
systemctl enable webapp.service
service webapp start

# Configure default user
echo "Create superuser login:"
python3 webapp/manage.py createsuperuser

# Static file setup
python3 webapp/manage.py collectstatic --noinput

echo "Setup complete"
echo "Serve HTTPS over localhost:443"
