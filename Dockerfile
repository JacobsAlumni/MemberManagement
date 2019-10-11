FROM python:3.6-alpine

# Install binary python dependencies
RUN apk add --no-cache \
    build-base \
    mailcap \
    libxslt-dev \
    linux-headers \
    pcre-dev \
    python3-dev

ADD docker/uwsgi.ini /app/uwsgi.ini

# Add requirements and install dependencies
ADD requirements.txt /app/
ADD requirements-prod.txt /app/
WORKDIR /app/

# Add the entrypoint and add configuration
RUN mkdir -p /var/www/static/ \
    && pip install -r requirements.txt \
    && pip install -r requirements-prod.txt

# Install Django App and setup the setting module
ADD manage.py /app/
ADD alumni/ /app/alumni
ADD django_forms_uikit/ /app/django_forms_uikit
ADD MemberManagement/ /app/MemberManagement
ADD registry/ /app/registry/
ADD static/ /app/static/
ADD custom_auth/ /app/custom_auth
ADD atlas/ /app/atlas
ADD payments/ /app/payments
ADD docker/ /app/docker

ENV DJANGO_SETTINGS_MODULE "MemberManagement.docker_settings"

### ALL THE CONFIGURATION

# disable / enable the devel warning shown on the page
ENV DJANGO_ENABLE_DEVEL_WARNING "1"

# The secret key used for django
ENV DJANGO_SECRET_KEY ""

# A comma-seperated list of allowed hosts
ENV DJANGO_ALLOWED_HOSTS "localhost"

# Database settings
## Use SQLITE out of the box
ENV DJANGO_DB_ENGINE "django.db.backends.sqlite3"
ENV DJANGO_DB_NAME "/data/MemberManagment.db"
ENV DJANGO_DB_USER ""
ENV DJANGO_DB_PASSWORD ""
ENV DJANG_DB_HOST ""
ENV DJANGO_DB_PORT ""

# Stripe keys -- required
ENV STRIPE_SECRET_KEY ""
ENV STRIPE_PUBLISHABLE_KEY ""

# GSuite Auth file should be in the data volume
ENV GOOGLE_ANALYTICS_ID ""
ENV GSUITE_AUTH_FILE /data/credentials.json

# Raven -- optional
ENV DJANGO_RAVEN_DSN ""

# Collect all the static files at build time
RUN DJANGO_SECRET_KEY=setup python manage.py collectstatic --noinput

# Volume and ports
VOLUME /data/
EXPOSE 80

ENTRYPOINT ["/app/docker/entrypoint.sh"]
CMD ["uwsgi", "--ini", "/app/docker/uwsgi.ini"]
