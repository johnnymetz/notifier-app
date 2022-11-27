"""
Gunicorn configuration file
https://docs.gunicorn.org/en/stable/configure.html#configuration-file
https://docs.gunicorn.org/en/stable/settings.html
https://adamj.eu/tech/2021/12/29/set-up-a-gunicorn-configuration-file-and-test-it/

Can verify config with: gunicorn api.wsgi:application --config python:api.gunicorn_conf --print-config

I tried putting this file in it's expected location (./gunicorn.conf.py)
but it broke `make pytest`.
"""
# import multiprocessing

max_requests = 1000
max_requests_jitter = 50

log_file = "-"

# This created 17 workers on heroku which lead to OOM issues.
# 1 worker default is fine for now.
# workers = multiprocessing.cpu_count() * 2 + 1

# Heroku has a 30 sec request timeout: https://devcenter.heroku.com/articles/request-timeout
# We want to set a gunicorn timeout well below the Heroku timeout so we don't
# create a situation outlined in the Heroku docs:
# While the router has returned a time out response to the client, your application
# will not know that the request it is processing  has reached a time-out, and your
# application will continue to work on the request.
timeout = 40
