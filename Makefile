DB_NAME=notifier
HEROKU_API_APP_NAME=notifier-app-api

all: shell

setup:
	pre-commit install

updateprecommit:
	pre-commit autoupdate
	pre-commit run --all-files

# BACKEND

pytest:
	docker-compose run api pytest

shell:
	# docker container exec -it notifier-app_api_1 bash
	# docker-compose exec api bash
	docker-compose run api bash

pyshell:
	docker-compose run api ./manage.py shell_plus --ipython -- --profile=me

logs:
	docker-compose logs -f --no-log-prefix api

dbshell:
	docker-compose exec db psql -U postgres

cleandb:
	docker-compose exec db psql -U postgres -c "DROP DATABASE ${DB_NAME} WITH (FORCE);"
	docker-compose exec db psql -U postgres -c "CREATE DATABASE ${DB_NAME};"

migratedb:
	docker-compose run api ./manage.py migrate

createsuperuser:
	@docker-compose run \
	  -e DJANGO_SUPERUSER_EMAIL=${MY_EMAIL} \
		-e DJANGO_SUPERUSER_PASSWORD=pw \
		api ./manage.py createsuperuser --noinput

importevents:
	docker-compose run api ./manage.py import_events ${MY_EMAIL}

exportevents:
	docker-compose run api ./manage.py export_events ${MY_EMAIL}

seeddb: migratedb createsuperuser importevents

pipcompile:
	docker-compose run api pip-compile

upgradepip:
	docker-compose run api pip-compile --upgrade

clear-silk:
	docker-compose run api ./manage.py silk_clear_request_log

# FRONTEND

cypress-open:
	npm run --prefix frontend/ cypress:open

cypress-run:
	npm run --prefix frontend/ cypress:run

cypress-docker-run:
	docker-compose -f docker-compose.yaml -f docker-compose.cypress.yaml up --abort-on-container-exit

# HEROKU

heroku-shell:
	heroku run -a ${HEROKU_API_APP_NAME} bash

heroku-logs:
	heroku logs -a ${HEROKU_API_APP_NAME} --tail

get-user-count:
	heroku run -a ${HEROKU_API_APP_NAME} bash -c 'echo "User.objects.count()" | python manage.py shell_plus --plain'

# MISCELLANEOUS

echoemail:
	echo ${MY_EMAIL}
