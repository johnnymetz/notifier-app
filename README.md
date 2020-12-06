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
./manage.py import_events EMAIL
./manage.py export_events EMAIL
./manage.py send_events_emails EMAIL

# development using email settings
docker-compose -f docker-compose.yaml -f docker-compose.email.yaml config
docker-compose -f docker-compose.yaml -f docker-compose.email.yaml up -d

# upgrade packages
pre-commit autoupdate
pre-commit run all-files
pip-compile upgrade  # then rebuild docker images
npm update
node and python versions  # Dockerfiles, heroku runtime, mypy config
```

## Todo

- Use direct type hints
- Add silk and/or django debug toolbar
- Address TODOs in code
- Change no year from 1000 to na or null or 0 or something else because older years are now supported
- Try an XSS attack: [XSS Exploitation in Django Applications](https://tonybaloney.github.io/posts/xss-exploitation-in-django.html)
- Add granulaized logging and ability to log sql when needed:

```
LOGGING = {
    # ...
    'loggers': {
        # ...
        'django.db': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

## Todo (maybe later)

- Sendgrid batch api
- Move config files to pyproject.toml
- Papertrail heroku plugin
- Unit test emails
- Try time-machine instead of freezegun: https://github.com/adamchainz/time-machine
- Integrate [django-migration-linter](https://github.com/3YOURMIND/django-migration-linter)

## Notes

- SendGrid: 100 free emails / day
- Heroku does not support SQLITE3
- PUT = full update; PATCH = partial update

```
# local vs utc datetime
dt_la = datetime.datetime.now(tz=pytz.timezone('America/Los_Angeles'))
dt_utc = dt_la.astimezone(pytz.utc)
```

## Heroku workflow

[heroku-buildpack-monorepo](https://elements.heroku.com/buildpacks/lstoll/heroku-buildpack-monorepo)

```
# deploy
git push frontend master
git push api master

# debug
heroku logs -a notifire-app --tail
heroku logs -a notifier-app-api --tail
heroku ps -a notifire-app
heroku ps -a notifier-app-api

# backend exec
heroku run -a notifier-app-api bash
heroku run -a notifier-app-api python manage.py send_events_emails EMAIL

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
git push https://git.heroku.com/notifire-app.git master
git remote add frontend https://git.heroku.com/notifire-app.git

# backend
heroku create -a notifier-app-api
heroku buildpacks:add -a notifier-app-api https://github.com/lstoll/heroku-buildpack-monorepo
heroku buildpacks:add -a notifier-app-api heroku/python
heroku buildpacks:add https://github.com/carloluis/heroku-buildpack-vim
heroku config:set -a notifier-app-api APP_BASE=api
git push https://git.heroku.com/notifier-app-api.git master
git remote add api https://git.heroku.com/notifier-app-api.git

# backend addons
heroku addons:create -a notifier-app-api heroku-postgresql:hobby-dev
heroku addons:create -a notifier-app-api scheduler:standard
# set env vars
```

## Djoser

```
./manage.py flush --noinput

# create user
http POST localhost:8000/api/auth/users/ email=$MY_EMAIL password=pw re_password=pw
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

## Resources

- [Production deployment checklist](https://testdriven.io/blog/production-django-deployments-on-heroku/)
- [SendGrid web api vs. SMTP](https://sendgrid.com/blog/web-api-or-smtp-relay-how-should-you-send-your-mail/)
  - Web api: [django-sendgrid-v5](https://github.com/sklarsa/django-sendgrid-v5) or [sendgrid-django](https://github.com/elbuo8/sendgrid-django)
  - SMPT: [no extra package necessary](https://sendgrid.com/docs/for-developers/sending-email/django/)
- [Using Postgres Row-Level Security in Python and Django](https://pganalyze.com/blog/postgres-row-level-security-django-python)
- [Installing system packages in Docker with minimal bloat](https://pythonspeed.com/articles/system-packages-docker/)

## iPython Notes

https://ipythonbook.com/

```
./manage.py shell_plus --ipython -- --profile=me
ipython locate me

%autoreload 2  # automatically reload modules so new session isn't required on code changes
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
