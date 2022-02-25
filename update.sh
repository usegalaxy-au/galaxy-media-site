#!/usr/bin/env bash

# Update Galaxy media site to latest commit on branch main

set -e

if [[ ! -f 'deploy/.venv/bin/activate' ]]; then
  echo "Could not find a virtualenv at ./deploy/.venv/"
  echo "If you have a virtual env configured at a different path, please soft link to it from this location."
  exit 1
fi

git pull
source deploy/.venv/bin/activate
cd webapp
python manage.py migrate || true
python manage.py collectstatic --noinput
sudo service webapp restart
