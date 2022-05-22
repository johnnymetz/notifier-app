"""
Gunicorn configuration file
https://docs.gunicorn.org/en/stable/configure.html#configuration-file
https://docs.gunicorn.org/en/stable/settings.html
https://adamj.eu/tech/2021/12/29/set-up-a-gunicorn-configuration-file-and-test-it/

Can verify config with: gunicorn api.wsgi:application --config python:gunicorn_conf --print-config

I tried putting this file in it's expected location (./gunicorn.conf.py)
but it broke `make pytest`.
"""
import multiprocessing

max_requests = 1000
max_requests_jitter = 50

log_file = "-"

workers = multiprocessing.cpu_count() * 2 + 1

timeout = 20
