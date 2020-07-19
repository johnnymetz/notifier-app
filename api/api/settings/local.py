from .base import *

SECRET_KEY = "12345"
DEBUG = True
ALLOWED_HOSTS = ["*"]

# https://github.com/anymail/django-anymail (try this?)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

CORS_ORIGIN_ALLOW_ALL = True

SIMPLE_JWT = {"ACCESS_TOKEN_LIFETIME": timedelta(minutes=1)}
