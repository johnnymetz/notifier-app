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

# heroku
git push heroku master
heroku run bash
heroku run python manage.py sendbirthdayemail jmetz

# heroku psql
heroku pg:psql
```

## Todo

- Deploy to monorepo to heroku
- Gmail mail is flakey (try SendGrid)
- Add cypress tests
- Add silk and/or django debug toolbar
- Unit test emails
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

## Monorepo deployment

```
# frontend
heroku create -a daily-notifier
heroku buildpacks:add -a daily-notifier https://github.com/lstoll/heroku-buildpack-monorepo
heroku buildpacks:add -a daily-notifier heroku/nodejs
heroku config:set -a daily-notifier APP_BASE=frontend
git push https://git.heroku.com/daily-notifier.git master

# frontend
heroku create -a notifier-app-api
heroku buildpacks:add -a notifier-app-api https://github.com/lstoll/heroku-buildpack-monorepo
heroku buildpacks:add -a notifier-app-api heroku/python
heroku config:set -a notifier-app-api APP_BASE=api
git push https://git.heroku.com/notifier-app-api.git master

# logs
heroku logs -a notifier-app-api --tail
heroku logs -a daily-notifier --tail

# heroku.yaml
heroku stack:set container -a notifier-application
heroku plugins:install @heroku-cli/plugin-manifest
git add/commit/push heroku master
heroku ps:scale web=1 worker=1
heroku addons:create cloudamqp:lemur
heroku addons:create heroku-postgresql:hobby-dev
heroku addons:create scheduler:standard

# set env vars

# scale dynos
heroku ps:scale web=1

# use paid dynos and add ssl
heroku ps:resize web=hobby
heroku certs:auto:enable
heroku certs:auto
```
