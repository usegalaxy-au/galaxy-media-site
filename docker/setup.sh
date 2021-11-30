# Config production server setup

# Webserver config
source .env
echo "Installing server configuration..."
sed "s/{{ HOSTNAME }}/$HOSTNAME/" nginx.conf.tmpl > nginx.conf
ln -s gunicorn.service /etc/systemd/system/webapp.service
ln -s gunicorn.socket /etc/systemd/system/webapp.socket
ln -s nginx.conf /etc/nginx/sites-available/webapp.conf
ln -s /etc/nginx/sites-available/webapp.conf /etc/nginx/sites-enabled/webapp
rm /etc/nginx/sites-enabled/default
echo "Running certbot to configure SSL certificates"
certbot --nginx -d $HOSTNAME

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
