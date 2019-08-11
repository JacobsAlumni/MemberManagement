# Member Management Portal

[![Build Status](https://travis-ci.org/JacobsAlumni/MemberManagement.svg?branch=master)](https://travis-ci.org/JacobsAlumni/MemberManagement)

The Django Application for managing Jacobs University Bremen Alumni Members. 

In general it fullfills six purposes: 

1. *Registration* of new Alumni Members
2. *Processing* of Applications
3. *Collection* of Membership fees
4. *Self-Updating* of Alumni Data
5. *Administration* of Alumni Data
6. *Searching* of Alumni Data

<small>(Side Note: If you can think of a good acroynym for these, let me know)</small>

## Installing

The entire application can be run locally for a development setup and via [Docker](https://www.docker.com/) in production. 

### Local Development Instance

To run a local instance, install Python 3.5 or newer, then clone this repository and afterwards set up a [virtal environment](https://docs.python.org/3/library/venv.html) as follows:

```bash
# Create and activate venv in venv/ 
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate
```

By default a local instance is then configured to store data in a local `db.sqlite3` database. 
Thus one can simply run the application like any other Django App using:

```bash
python manage.py runserver
```


In principle the settings can be found in [`settings.py`](MemberManagement/settings.py). 
To enable easier debugging, it is configured to automatically import settings from a file called `MemberManagement/local_settings.py`.
This file is intended to contain local settings, such as session tokens, or external authentication credentials. 
The file is also `.gitignore`d and should not be comitted. 

Notice that however because of external integrations, some features may not work as expected. 
See the Configuration sections of the appropriate settings to configure. 

### Deployment via Docker

It is also possible to deploy this application via [Docker](https://www.docker.com/). 
Concretly, this repository is available as the [automated build](https://docs.docker.com/v17.12/docker-cloud/builds/automated-build/) [`jacobsalumni/membermanagement`](https://hub.docker.com/r/jacobsalumni/membermanagement/). 

For Docker purposes the configuration file `MemberManagement/local_settings.py` is used.  
By default, it also uses a local sqlite database. 
All configuration can be set via environment variables, see [Dockerfile](Dockerfile) for details. 

## Code Structure

The code is layed out as any other Django app.
The entry point can be found in `MemberManagement`. 

The following portal-related apps exist:

- `MemberManagement/` -- serves as an entry point, contains all static routes and base templates
- `registry/` -- user-facing registration + editing of data (purposes 1 + 4)
- `alumni/` -- admin-facing viewing + editing of data, contains core Alumni models (purpose 5)
- `custom_auth/` -- GSuite-integration, including login and approval (purpose 2)
- `payments/` -- Stripe + payments integration (purpose 3)
- `atlas/` -- user-facing search of atlas data (purpose 6)

The following independent apps also exist:

- `django_forms_uikit` -- rendering django forms using the uikit framework

## Tests

Tests are in the process of being set up. 

One non-feature related test is the CodeStyle test. This enforces PEP8-compliance except for maximum line length.

## License
Licensed under the Terms of the MIT LICENSE, see [LICENSE](LICENSE). 
