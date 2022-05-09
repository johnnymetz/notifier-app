import rollbar

from .base import *

SECRET_KEY = "DONOTUSEINPRODUCTION"  # nosec
DEBUG = True
ALLOWED_HOSTS = ["*"]
CORS_ORIGIN_ALLOW_ALL = True

AUTH_PASSWORD_VALIDATORS = []

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=20),
    "REFRESH_TOKEN_LIFETIME": timedelta(hours=1),
}

# django-templated-mail
DOMAIN = "localhost:3001"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"rich": {"datefmt": "[%X]"}},
    "handlers": {
        "console": {
            "class": "rich.logging.RichHandler",
            "formatter": "rich",
            "level": "DEBUG",
        }
    },
    "loggers": {"django": {"handlers": ["console"]}},
}


# https://docs.rollbar.com/docs/django
ROLLBAR = {
    "enabled": os.environ.get("ROLLBAR_ENABLED", "").lower() == "true",
    "access_token": os.environ.get("ROLLBAR_ACCESS_TOKEN"),
    "environment": "development",
    "root": BASE_DIR,
    "branch": "main",
    "capture_email": True,
    "capture_username": True,
}
rollbar.init(**ROLLBAR)
