# Contributing

## Basic Setup

```
# initial setup (only needs to be done once)
brew install pre-commit
pre-commit install

# set environment variables
export MY_EMAIL=<YOUR_EMAIL>

# development using local settings
docker compose up -d
docker container exec -it notifier-app_api_1 bash
./manage.py migrate
./manage.py createsuperuser
./manage.py import_events EMAIL
./manage.py export_events EMAIL
./manage.py send_event_emails EMAIL
```

Now visit http://localhost:3001/ and login with `<YOUR_EMAIL>` and `pw`.

## Upgrade packages

```
# pre-commit
make updateprecommit  # runs all hooks for us

# Python version
Dockerfile
pyproject.toml black + mypy
runtime.txt for heroku  # see supported runtimes below
pyupgrade argument

# watchman version
Dockerfile

# backend packages
make pipcompileupgrade
make pytest
.pre-commit-config.yaml  # update django-upgrade target version

# Node version
frontend/Dockerfile
frontend/Dockerfile.dev
package.json > engines > node

# frontend packages
npm install
npm list --depth 0

# update frontend packages:
npm install -g npm-check-updates
ncu  # show all updates
# SKIP:
# - bootstrap: still on v4 (latest is v5)
# - cypress: upgrade separately (see below)
ncu --reject bootstrap,\
react-bootstrap\
cypress

# cypress version
package.json
docker-compose.cypress.yaml
```

- [Heroku Python Support](https://devcenter.heroku.com/articles/python-support#supported-runtimes)
- Be sure to rebuild docker images, run pre-commit hooks, run unit tests and run cypress tests against all files after an upgrade.

## New Relic

Set the following environment variables:

```
NEW_RELIC_LICENSE_KEY=df78d9296c9e9cb6f08b48c86cfe01cfbf00NRAL
NEW_RELIC_CONFIG_FILE=newrelic.ini
```

## Development using email settings

Use this if you want to send actual emails instead of logging them to the api container.

```
# set environment variables
export DEFAULT_FROM_EMAIL="Notifier App <YOUR_EMAIL>"
export SENDGRID_API_KEY=<YOUR_KEY>

# spin up containers
docker compose -f docker-compose.yaml -f docker-compose.email.yaml config
docker compose -f docker-compose.yaml -f docker-compose.email.yaml up -d
```

## Run Cypress Tests

```
# set environment variables
export CYPRESS_QA_USER_EMAIL1=<SOME_EMAIL>
export CYPRESS_QA_USER_EMAIL2=<ANOTHER_EMAIL>
export CYPRESS_QA_USER_PASSWORD=<A_RANDOM_PASSWORD>

# cypress open
export CYPRESS_BASE_URL=http://localhost:3001
export CYPRESS_SERVER_URL=http://localhost:8000/api
make host-cypress-open

# cypress run
make docker-cypress-run
```

## Heroku workflow

```
# deploy (automatic deploys from main are enabled)
git push

# debug
heroku logs -a notifier-app-api --tail
heroku ps -a notifier-app-api

# backend exec
heroku run -a notifier-app-api bash
heroku run -a notifier-app-api python manage.py send_event_emails EMAIL

# check production settings on heroku server
./manage.py check --deploy --settings api.settings.production

# psql
heroku pg:psql
```

## Notes

- SendGrid: 100 free emails / day
- PUT = full update; PATCH = partial update

```
# local vs utc datetime
dt_la = datetime.datetime.now(tz=pytz.timezone('America/Los_Angeles'))
dt_utc = dt_la.astimezone(pytz.utc)
```

## Djoser

```bash
./manage.py flush --noinput

# create user
http POST localhost:8000/api/auth/users/ email=$MY_EMAIL password=pw re_password=pw

# get token
export TOKEN=$(http POST localhost:8000/api/auth/jwt/create/ email=$MY_EMAIL password=pw | jq -r '.access')

# send authenticated request
http OPTIONS http://localhost:8000/api/events/ Authorization:"Bearer $TOKEN"
```

### Endpoints tested / implemeneted in UI

- [x] Get current user
- [x] Create user
- [x] Activate user
- [ ] Resend activation email
- [x] Update/patch user
- [ ] Delete user
- [x] Set username (aka email)
- [x] Set password
- [ ] Send reset username (aka email) email
- [ ] Reset forgotten username (aka email)
- [x] Send reset password email
- [x] Reset forgotten password
- [x] JWT create
- [x] JWT verify
- [x] JWT refresh

## iPython Notes

[ipythonbook](https://ipythonbook.com/)

```
./manage.py shell_plus --ipython -- --profile=me
ipython locate me

# automatically reload modules so new session isn't required on code changes
%autoreload 2

%env
%hist -n
%lsmagic
%magic -brief
help(random.randint)
random.randint?
random.randint??
%quickref
%recall 3
%rerun 3
%timeit square(2)
%who
%whos
%whos str
```

## Notes

- Find celery code by searching for commit description "Remove unused celery stuff"
