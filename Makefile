setup:
	pre-commit install

# BACKEND

pytest:
	@docker-compose run api pytest --ds=api.settings.test

shell:
	# docker container exec -it notifier-app_api_1 bash
	# @docker-compose exec api bash
	@docker-compose run api bash

pyshell:
	@docker-compose run api ./manage.py shell_plus --ipython -- --profile=me

logs:
	docker container logs -f notifier-app_api_1

dbshell:
	PGPASSWORD=postgres psql -h localhost -U postgres -d notifier -p 5433

migratedb:
	@docker-compose run api ./manage.py migrate

seeddb:
	@docker-compose run api ./manage.py migrate
	@docker-compose run \
	  -e DJANGO_SUPERUSER_EMAIL=${MY_EMAIL} \
		-e DJANGO_SUPERUSER_PASSWORD=pw \
		api ./manage.py createsuperuser --noinput
	@docker-compose run api ./manage.py import_events ${MY_EMAIL}

cleandb:
	# kill any existing sessions connected to db
	# PGPASSWORD=postgres psql -h localhost -U postgres -p 5433 -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE pid IN (SELECT pid FROM pg_stat_activity WHERE datname = 'notifier');"
	PGPASSWORD=postgres psql -h localhost -U postgres -p 5433 -c "DROP DATABASE notifier WITH (FORCE);"
	PGPASSWORD=postgres psql -h localhost -U postgres -p 5433 -c "CREATE DATABASE notifier;"

pipcompile:
	@docker-compose run api pip-compile

clear-silk:
	@docker-compose run api ./manage.py silk_clear_request_log

heroku-shell:
	heroku run -a notifier-app-api bash

heroku-logs:
	heroku logs -a notifier-app-api --tail

# FRONTEND

cypress-open:
	npm run --prefix frontend/ cypress:open

cypress-run:
	npm run --prefix frontend/ cypress:run

# MISCELLANEOUS

get-user-count:
	heroku run -a notifier-app-api bash -c 'echo "User.objects.count()" | python manage.py shell_plus --plain'

echo:
	echo ${MY_EMAIL}
