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
api/Dockerfile
api/pyproject.toml black + mypy
api/runtime.txt for heroku  # see supported runtimes below
pyupgrade argument

# watchman version
api/Dockerfile

# backend packages
make pipcompileupgrade
make pytest

# Node version
frontend/Dockerfile
frontend/Dockerfile.dev
package.json > engines > node  # https://devcenter.heroku.com/articles/nodejs-support#specifying-a-node-js-version

# frontend packages
npm install -g npm-check-updates
ncu  # show any updates
ncu -u cypress  # update cypress in package.json
ncu -u  # update all in package.json
npm install
npm list --depth 0
# cypress
image in docker-compose.cypress.yaml
```

- [Heroku Python Support](https://devcenter.heroku.com/articles/python-support#supported-runtimes)
- Be sure to rebuild docker images, run pre-commit hooks, run unit tests and run cypress tests against all files after an upgrade.

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

[heroku-buildpack-monorepo](https://elements.heroku.com/buildpacks/lstoll/heroku-buildpack-monorepo)

```
# deploy
git remote add frontend https://git.heroku.com/notifire-app.git
git remote add api https://git.heroku.com/notifier-app-api.git
git push frontend main
git push api main

# debug
heroku logs -a notifire-app --tail
heroku logs -a notifier-app-api --tail
heroku ps -a notifire-app
heroku ps -a notifier-app-api

# backend exec
heroku run -a notifier-app-api bash
heroku run -a notifier-app-api python manage.py send_event_emails EMAIL

# check production settings on heroku server
./manage.py check --deploy --settings api.settings.production

# psql
heroku pg:psql
```

## Heroku monorepo setup

```
# frontend
heroku create -a notifire-app
heroku buildpacks:add -a notifire-app https://github.com/lstoll/heroku-buildpack-monorepo
heroku buildpacks:add -a notifire-app heroku/nodejs
heroku config:set -a notifire-app APP_BASE=frontend
git push https://git.heroku.com/notifire-app.git main
git remote add frontend https://git.heroku.com/notifire-app.git

# backend
heroku create -a notifier-app-api
heroku buildpacks:add -a notifier-app-api https://github.com/lstoll/heroku-buildpack-monorepo
heroku buildpacks:add -a notifier-app-api heroku/python
heroku buildpacks:add https://github.com/carloluis/heroku-buildpack-vim
heroku config:set -a notifier-app-api APP_BASE=api
git push https://git.heroku.com/notifier-app-api.git main
git remote add api https://git.heroku.com/notifier-app-api.git

# backend addons
heroku addons:create -a notifier-app-api heroku-postgresql:hobby-dev
heroku addons:create -a notifier-app-api scheduler:standard
# set env vars
```

## Notes

- SendGrid: 100 free emails / day
- Heroku does not support SQLITE3
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
