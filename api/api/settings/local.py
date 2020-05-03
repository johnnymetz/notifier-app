from .base import *

SECRET_KEY = "12345"

DEBUG = True

# EMAIL
# https://github.com/anymail/django-anymail (try this?)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
