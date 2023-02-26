"""
./manage.py check --deploy --settings api.settings.production
"""
import dj_database_url
import rollbar
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *

# General
SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = False
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(" ")
CORS_ORIGIN_WHITELIST = os.environ.get("CORS_ORIGIN_WHITELIST", "").split(" ")

# Database
DATABASE_URL = os.environ.get("DATABASE_URL")
db_from_env = dj_database_url.config(
    default=DATABASE_URL, conn_max_age=500, ssl_require=True
)
DATABASES["default"].update(db_from_env)

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Email
EMAIL_BACKEND = "anymail.backends.sendgrid.EmailBackend"
DEFAULT_FROM_EMAIL = os.environ["DEFAULT_FROM_EMAIL"]
ANYMAIL = {"SENDGRID_API_KEY": os.environ["SENDGRID_API_KEY"]}

# django-templated-mail
DOMAIN = os.environ["DOMAIN"]

# Security
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_HSTS_SECONDS = 30
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

REST_FRAMEWORK["DEFAULT_PERMISSION_CLASSES"] = (
    "rest_framework.permissions.IsAuthenticated",
)
REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"] = {
    # rates recommended by docs
    "anon": "100/day",
    "user": "1000/day",
}

# https://docs.rollbar.com/docs/django
ROLLBAR = {
    "access_token": os.environ.get("ROLLBAR_ACCESS_TOKEN"),
    "environment": "production",
    "root": str(BASE_DIR),
    "branch": "main",
    "capture_email": True,
    "capture_username": True,
}
rollbar.init(**ROLLBAR)

# sentry
sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    integrations=[DjangoIntegration()],
    environment="production",
    traces_sample_rate=1.0,
    send_default_pii=False,  # associate users to errors
)


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
        },
    },
    "loggers": {
        "play": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}