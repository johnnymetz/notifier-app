# Notifier App

## Development

```
# initial setup (only needs to be done once)
pip-compile
pip-sync
pre-commit install

# development using local settings
docker-compose up -d
docker container exec -it notifier-app_api_1 bash
# migrate run as part of startup command
./manage.py createsuperuser  # fill out email
./manage.py addfriends USERNAME
./manage.py sendbirthdayemail USERNAME

# development using gmail settings
docker-compose -f docker-compose.yaml -f docker-compose.gmail.yaml config
docker-compose -f docker-compose.yaml -f docker-compose.gmail.yaml up -d

# setup db
./manage.py migrate
./manage.py createsuperuser
./manage.py addfriends USERNAME

# send test email
./manage.py sendbirthdayemail USERNAME
```

## Todo

- Add user management (registration, password reset, etc.)
- Gmail mail is flakey (try SendGrid)
- Unit test emails
- Fix list vs object permissions

## Todo (maybe later)

- Add cypress tests
- Add silk and/or django debug toolbar
- [Pytz deprecation guide](https://pytz-deprecation-shim.readthedocs.io/en/latest/migration.html#which-replacement-to-choose)

## Notes

- SendGrid: 100 free emails / day
- Heroku does not support SQLITE3
- [Production deployment checklist](https://testdriven.io/blog/production-django-deployments-on-heroku/)
- PUT = full update; PATCH = partial update

```
# local vs utc datetime
dt_la = datetime.datetime.now(tz=pytz.timezone('America/Los_Angeles'))
dt_utc = dt_la.astimezone(pytz.utc)
```

## Heroku monorepo deployment

[heroku-buildpack-monorepo](https://elements.heroku.com/buildpacks/lstoll/heroku-buildpack-monorepo)

```
# frontend
heroku create -a daily-notifier
heroku buildpacks:add -a daily-notifier https://github.com/lstoll/heroku-buildpack-monorepo
heroku buildpacks:add -a daily-notifier heroku/nodejs
heroku config:set -a daily-notifier APP_BASE=frontend
git push https://git.heroku.com/daily-notifier.git master

# backend
heroku create -a notifier-app-api
heroku buildpacks:add -a notifier-app-api https://github.com/lstoll/heroku-buildpack-monorepo
heroku buildpacks:add -a notifier-app-api heroku/python
heroku config:set -a notifier-app-api APP_BASE=api
git push https://git.heroku.com/notifier-app-api.git master

# debug
heroku logs -a daily-notifier --tail
heroku logs -a notifier-app-api --tail
heroku ps -a daily-notifier
heroku ps -a notifier-app-api

# backend addons
heroku addons:create -a notifier-app-api heroku-postgresql:hobby-dev
heroku addons:create -a notifier-app-api scheduler:standard
# set env vars

# backend exec
heroku run -a notifier-app-api bash
heroku run -a notifier-app-api python manage.py sendbirthdayemail jmetz

# psql
heroku pg:psql
```
