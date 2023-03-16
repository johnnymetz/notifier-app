release: ./manage.py migrate; ./manage.py collectstatic --noinput

web: ./manage.py check --deploy; newrelic-admin run-program gunicorn api.wsgi:application --bind=0.0.0.0:$PORT --config python:api.gunicorn_conf
