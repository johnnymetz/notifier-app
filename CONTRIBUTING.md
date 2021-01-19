# Contributing

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

# upgrade packages
pre-commit autoupdate
pre-commit run --all-files
pip-compile upgrade  # then rebuild docker images
npm update
node and python versions  # Dockerfiles, heroku runtime, mypy config
```
