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
./manage.py migrate
./manage.py createsuperuser
./manage.py addfriends USERNAME
./manage.py sendbirthdayemail USERNAME

# development using prod settings
docker-compose -f docker-compose.yaml -f docker-compose.prod.yaml config
docker-compose -f docker-compose.yaml -f docker-compose.prod.yaml up -d

# setup db
./manage.py migrate
./manage.py createsuperuser
./manage.py addfriends USERNAME

# send test email
./manage.py sendbirthdayemail USERNAME
```

## Todo

- Add django debug toolbar
- Unit test emails
- [Production deployment checklist](https://testdriven.io/blog/production-django-deployments-on-heroku/)
- Optimize/secure admin

## Notes

- Heroku does not support SQLITE3

```
# local vs utc datetime
dt_la = datetime.datetime.now(tz=pytz.timezone('America/Los_Angeles'))
dt_utc = dt_la.astimezone(pytz.utc)
```
