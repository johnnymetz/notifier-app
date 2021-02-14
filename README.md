# Notifier App

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge)](https://github.com/psf/black)
[![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg?style=for-the-badge)](https://github.com/prettier/prettier)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&style=for-the-badge)](https://github.com/pre-commit/pre-commit)

![Django](https://img.shields.io/badge/-Django-092E20?logo=Django&style=for-the-badge)
![PostgreSQL](https://img.shields.io/badge/postgres-%23316192.svg?logo=postgresql&style=for-the-badge)
![React](https://img.shields.io/badge/react%20-%2320232a.svg?logo=react&style=for-the-badge)
![Bootstrap](https://img.shields.io/badge/-Bootstrap-563D7C?logo=bootstrap&style=for-the-badge)
![Heroku](https://img.shields.io/badge/heroku%20-%23430098.svg?logo=heroku&style=for-the-badge)
![Docker](https://img.shields.io/badge/docker%20-%230db7ed.svg?logo=docker&logoColor=white&style=for-the-badge)

Send yourself email notifications every day.

## Todo

- Upgrade djoser so activation email isn't sent on user update (e.g. subscribe on/off)
- Use direct type hints (once mypy supports it)
- Address TODOs in code
- Finish [flake8 plugins](https://dev.to/bowmanjd/some-flake8-plugins-for-python-linting-107h):
  - flake8-bandit
  - Others from [flake8-awesome](https://github.com/afonasev/flake8-awesome)
- Try an XSS attack: [XSS Exploitation in Django Applications](https://tonybaloney.github.io/posts/xss-exploitation-in-django.html)

## Todo (maybe later)

- Move config files to pyproject.toml
- Papertrail heroku plugin
- Add [django-version-checks](https://github.com/adamchainz/django-version-checks)
  - Ensures all devs are have the correct environment setup
- Sendgrid batch api
- Unit test emails
- Freezegun should be able to choose a timezone
  so I don't need to set settings.TIME_ZONE = "UTC" in the first line of every test
- Try [time-machine](https://github.com/adamchainz/time-machine) instead of freezegun
- Integrate [django-migration-linter](https://github.com/3YOURMIND/django-migration-linter)
- PR in django-extensions to raise error on `create_command` if file already exists
- Scan site with [Mozilla Observatory](https://observatory.mozilla.org/)
- [Add security.txt to .well-known endpoint](https://adamj.eu/tech/2020/06/28/how-to-add-a-well-known-url-to-your-django-site/)
- [Maybe add robots endpoint](https://adamj.eu/tech/2020/02/10/robots-txt/)
- Create splash page
- Add holidays

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
  - Web api:
    - [django-sendgrid-v5](https://github.com/sklarsa/django-sendgrid-v5)
    - (OR) [sendgrid-django](https://github.com/elbuo8/sendgrid-django)
  - SMPT: [no extra package necessary](https://sendgrid.com/docs/for-developers/sending-email/django/)
- [Using Postgres Row-Level Security in Python and Django](https://pganalyze.com/blog/postgres-row-level-security-django-python)
- [Installing system packages in Docker with minimal bloat](https://pythonspeed.com/articles/system-packages-docker/)
- [super-linter](https://github.com/github/super-linter)

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
