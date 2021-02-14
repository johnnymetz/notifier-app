# Contributing

## Basic Setup

```
# initial setup (only needs to be done once)
brew install pre-commit
pre-commit install

# development using local settings
docker-compose up -d
docker container exec -it notifier-app_api_1 bash
./manage.py migrate
./manage.py createsuperuser
./manage.py import_events EMAIL
./manage.py export_events EMAIL
./manage.py send_event_emails EMAIL

# development using email settings
docker-compose -f docker-compose.yaml -f docker-compose.email.yaml config
docker-compose -f docker-compose.yaml -f docker-compose.email.yaml up -d

# run cypress tests in docker container
docker-compose -f docker-compose.yaml -f docker-compose.cypress.yaml up --abort-on-container-exit

# upgrade packages
pre-commit autoupdate
pre-commit run --all-files
pip-compile upgrade  # then rebuild docker images
npm update
node and python versions  # Dockerfiles, heroku runtime, mypy config
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
