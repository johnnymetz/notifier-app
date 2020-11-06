setup:
	pre-commit install

shell:
	docker container exec -it notifier-app_api_1 bash

pyshell:
	@docker-compose exec api ./manage.py shell_plus --ipython

dbshell:
	PGPASSWORD=postgres psql -h localhost -U postgres -d notifier

logs:
	docker container logs -f notifier-app_api_1

pytest:
	@docker-compose exec api pytest

dbseed:
	@docker-compose exec api ./manage.py migrate
	@docker-compose exec api ./manage.py createsuperuser --email ${MY_EMAIL}
	@docker-compose exec api ./manage.py import_friends ${MY_EMAIL}

cleandb:
	# kill any existing sessions connected to db
	# PGPASSWORD=postgres psql -h localhost -U postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE pid IN (SELECT pid FROM pg_stat_activity WHERE datname = 'notifier');"
	# may need "WITH (FORCE)" in the drop db command (or the command above) for this to work
	PGPASSWORD=postgres psql -h localhost -U postgres -c "DROP DATABASE notifier;"
	PGPASSWORD=postgres psql -h localhost -U postgres -c "CREATE DATABASE notifier;"

echo:
	echo ${MY_EMAIL}

pipcompile:
	@docker-compose exec api pip-compile
