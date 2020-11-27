setup:
	pre-commit install

# BACKEND

test:
	@docker-compose exec api pytest

shell:
	docker container exec -it notifier-app_api_1 bash

pyshell:
	@docker-compose exec api ./manage.py shell_plus --ipython -- --profile=me

logs:
	docker container logs -f notifier-app_api_1

dbshell:
	PGPASSWORD=postgres psql -h localhost -U postgres -d notifier

dbmigrate:
	@docker-compose exec api ./manage.py migrate

dbseed:
	@docker-compose exec api ./manage.py migrate
	@docker-compose exec api ./manage.py createsuperuser --email ${MY_EMAIL}
	@docker-compose exec api ./manage.py import_friends ${MY_EMAIL}

cleandb:
	# kill any existing sessions connected to db
	# PGPASSWORD=postgres psql -h localhost -U postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE pid IN (SELECT pid FROM pg_stat_activity WHERE datname = 'notifier');"
	PGPASSWORD=postgres psql -h localhost -U postgres -c "DROP DATABASE notifier WITH (FORCE);"
	PGPASSWORD=postgres psql -h localhost -U postgres -c "CREATE DATABASE notifier;"

pipcompile:
	@docker-compose exec api pip-compile

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
