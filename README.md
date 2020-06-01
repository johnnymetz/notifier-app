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
./manage.py createsuperuser
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
```

## Todo

- Add cypress tests
- Add silk or django debug toolbar
- Unit test emails

## Notes

- Heroku does not support SQLITE3
- [Production deployment checklist](https://testdriven.io/blog/production-django-deployments-on-heroku/)

```
# local vs utc datetime
dt_la = datetime.datetime.now(tz=pytz.timezone('America/Los_Angeles'))
dt_utc = dt_la.astimezone(pytz.utc)
```

## Deployment

```
# initial setup
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
