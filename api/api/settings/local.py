from .base import *

# General
SECRET_KEY = "12345"
DEBUG = True

# Email
# https://github.com/anymail/django-anymail (try this?)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
