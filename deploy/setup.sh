# Config production server setup

set -e

# Drop into ./deploy if user called from root dir
[[ -d deploy ]] && [[ -d webapp ]] && cd deploy

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

echo ""
echo "Installing system dependancies..."
sudo apt-get update \
&& sudo apt-get install -y --no-install-recommends \
    python3.8 \
    python3-pip \
    postgresql-client \
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
sed "s|{{ PWD }}|$PWD|" gunicorn.service.tmpl > gunicorn.service
sudo ln -s gunicorn.service /etc/systemd/system/webapp.service
sudo ln -s gunicorn.socket /etc/systemd/system/webapp.socket
sudo ln -s nginx.conf /etc/nginx/sites-available/webapp.conf
sudo ln -s /etc/nginx/sites-available/webapp.conf /etc/nginx/sites-enabled/webapp
sudo ln -s "$(dirname $PWD)/webapp /srv/sites/webapp"
sudo rm /etc/nginx/sites-enabled/default

echo ""
if [[ $ssl = 'y' ]]; then
    echo "Configuring SSL with Certbot..."
    sudo certbot --nginx -d $HOSTNAME
elif [[ $ssl = 'n' ]]; then
    echo "Skipping SSL..."
fi

# Set up database
echo ""
echo "Configuring database"
sudo su postgres
sudo -u postgres createuser $DB_USER
sudo -u postgres createdb $DB_NAME
sudo -u postgres psql << SQL
ALTER USER $DB_NAME WITH PASSWORD $DB_PASSWORD;
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
SQL

# Start services\
echo ""
echo "Reloading system services..."
sudo service nginx restart
sudo service postgresql restart
sudo systemctl enable webapp.socket
sudo systemctl enable webapp.service
sudo service webapp start

# Configure default user
echo ""
echo "Create superuser login:"
python3.8 webapp/manage.py createsuperuser

# Static file setup
python3.8 webapp/manage.py collectstatic --noinput

echo "Setup complete"
case $ssl in
    "y" )   echo "Serving HTTPS at $HOSTNAME";;
    "n" )   echo "Serving HTTP at $HOSTNAME";;
esac
echo ""
