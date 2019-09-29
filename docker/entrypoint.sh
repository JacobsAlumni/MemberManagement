#!/bin/sh
set -e

# run database migrations
python manage.py migrate --noinput

# startup with whatever command was provided
"$@"