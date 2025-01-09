# Maintenance page

Show this when the main site is offline for maintenance/outage.

- Make sure that this directory is symlinked to `/srv/sites/gms-maintenance-site/`
- Move the selected Nginx config to your /etc/nginx/sites-enabled/ to replace
  the production nginx config.
- Make sure that the SSL cert paths defined in the nginx config exist on your
  server (they should have be created with python-certbot-nginx) - they can be
  tarred and copied from the main web server if running this somewhere else
  (e.g. infra outage).
- `sudo systemctl nginx restart`
