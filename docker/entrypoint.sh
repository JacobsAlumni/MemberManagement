#!/bin/sh

# Update static files
python manage.py collectstatic --noinput

# Run Migrations
python manage.py migrate --noinput

# If a parameter is given, run a manage.py command
# e.g. run 'createsuperuser' to create a super user
#if ! [ -z "$1" ]; then
#    python manage.py $@
#    exit $?
#fi;


# Start gunicorn for wsgi on localhost:8000
gunicorn MemberManagement.wsgi:application --bind 127.0.0.1:8000 &

# Run nginx with django configuration
nginx -c /etc/nginx/django.conf