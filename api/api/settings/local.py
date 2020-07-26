from .base import *

SECRET_KEY = "12345"
DEBUG = True
ALLOWED_HOSTS = ["*"]
CORS_ORIGIN_ALLOW_ALL = True

AUTH_PASSWORD_VALIDATORS = []

# https://github.com/anymail/django-anymail (try this?)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(hours=1),
}
