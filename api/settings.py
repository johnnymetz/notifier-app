import sys
import typing
from datetime import timedelta
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

import dj_database_url
import environ
import rollbar
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

ENV_LOCAL = "local"
ENV_PRODUCTION = "production"
ENV_NAMES = {ENV_LOCAL, ENV_PRODUCTION}

env = environ.Env(
    ALLOWED_HOSTS=(str, ""),
    CORS_ORIGIN_WHITELIST=(str, ""),
    CYPRESS_AUTH_SECRET=(str, ""),
    CYPRESS_QA_USER_EMAIL1=(str, None),
    CYPRESS_QA_USER_EMAIL2=(str, None),
    CYPRESS_QA_USER_PASSWORD=(str, None),
    DATABASE_URL=(str, "postgres://postgres:postgres@localhost:5432/postgres"),
    DATABASE_REQUIRE_SSL=(bool, True),
    DEBUG=(bool, False),
    DEFAULT_FROM_EMAIL=(str, "Notifier App <admin@example.com>"),
    ENVIRONMENT_NAME=(str, None),
    FRONTEND_URL=(str, ""),
    ROLLBAR_ACCESS_TOKEN=(str, None),
    ROLLBAR_ENABLED=(bool, False),
    SENDGRID_API_KEY=(str, None),
    SENTRY_DSN=(str, None),
    SENTRY_ENABLED=(bool, False),
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


ENV_FILE = BASE_DIR / ".env"

if ENV_FILE.exists():
    environ.Env.read_env(ENV_FILE)

TESTING = "pytest" in sys.modules

ENVIRONMENT_NAME = env("ENVIRONMENT_NAME")

if ENVIRONMENT_NAME and ENVIRONMENT_NAME not in ENV_NAMES:
    raise ImproperlyConfigured(f"Invalid ENVIRONMENT_NAME: {ENVIRONMENT_NAME}")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# In GitHub CI, settings are initialized with DEBUG=False (even though django_debug_mode=true),
# so do NOT use DEBUG to conditionally set other settings
DEBUG = env("DEBUG")

if DEBUG and ENVIRONMENT_NAME == ENV_PRODUCTION:
    raise ImproperlyConfigured("DEBUG=True in production")

ALLOWED_HOSTS = [x.strip() for x in env.list("ALLOWED_HOSTS")]

FRONTEND_URL = env("FRONTEND_URL")

CORS_ORIGIN_WHITELIST = [FRONTEND_URL]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # third-party
    "django_extensions",
    "corsheaders",
    "rest_framework",
    "djoser",
    "drf_yasg",
    # my apps
    "users.apps.UsersConfig",
    "notifier.apps.NotifierConfig",
    "play.apps.PlayConfig",
]

MIDDLEWARE = [
    # rollbar Only404 should be first
    "rollbar.contrib.django.middleware.RollbarNotifierMiddlewareOnly404",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "api.middleware.ReportFailedCORSPreflightMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # rollbar Excluding404 or the single middleware should be last
    "rollbar.contrib.django.middleware.RollbarNotifierMiddlewareExcluding404",
]

ROOT_URLCONF = "api.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "api.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# mypy was complaining about ATOMIC_REQUESTS=True
DATABASES: dict[str, typing.Any]

if TESTING:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": str(BASE_DIR / "db.sqlite3"),
        }
    }
else:
    DATABASE_URL = env("DATABASE_URL")

    if not DATABASE_URL:
        raise ImproperlyConfigured("DATABASE_URL is not set")

    DATABASES = {
        "default": {
            **dj_database_url.parse(
                DATABASE_URL, ssl_require=env("DATABASE_REQUIRE_SSL")
            ),
            "ENGINE": "django.db.backends.postgresql",
            "ATOMIC_REQUESTS": True,
        }
    }

AUTH_USER_MODEL = "users.User"

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = (
    [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        },
        {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
        {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
        {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
    ]
    if ENVIRONMENT_NAME == ENV_PRODUCTION
    else []
)


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/Los_Angeles"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
# https://devcenter.heroku.com/articles/django-assets

STATIC_URL = "/staticfiles/"

STATIC_ROOT = BASE_DIR / "static"

# Security
if ENVIRONMENT_NAME == ENV_PRODUCTION:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_HSTS_SECONDS = 30
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"


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
        "api.telemetry": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "play": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

# https://www.willmcgugan.com/blog/tech/post/richer-django-logging/
if ENVIRONMENT_NAME == ENV_LOCAL:
    LOGGING["formatters"] = {"rich": {"datefmt": "[%X]"}}
    LOGGING["handlers"]["rich"] = {  # type: ignore
        "class": "rich.logging.RichHandler",
        "formatter": "rich",
        "level": "DEBUG",
    }
    LOGGING["loggers"]["django"] = {"handlers": ["rich"]}  # type: ignore


if TESTING:
    INSTALLED_APPS.append("nplusone.ext.django")
    MIDDLEWARE.insert(0, "nplusone.ext.django.NPlusOneMiddleware")
    NPLUSONE_RAISE = True


# Email
EMAIL_BACKEND = (
    "django.core.mail.backends.console.EmailBackend"
    # See DEBUG for why we're using ENVIRONMENT_NAME instead of DEBUG
    if ENVIRONMENT_NAME == ENV_LOCAL
    else "anymail.backends.sendgrid.EmailBackend"
)
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")
ANYMAIL = {"SENDGRID_API_KEY": env("SENDGRID_API_KEY")}

# django-templated-mail (used by djoser)
DOMAIN = FRONTEND_URL
SITE_NAME = "Notifire"


SWAGGER_SETTINGS = {
    "USE_SESSION_AUTH": False,
    "SECURITY_DEFINITIONS": {
        "Token": {"type": "apiKey", "name": "Authorization", "in": "header"}
    },
}


REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "api.pagination.CustomPageNumberPagination",
    "PAGE_SIZE": 5,
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    # Only works with rest_framework.test.APIClient + rest_framework.test.APIRequestFactory
    # "TEST_REQUEST_DEFAULT_FORMAT": "json",
    # Includes parsed POST variables in exception
    "EXCEPTION_HANDLER": "rollbar.contrib.django_rest_framework.post_exception_handler",
}

if ENVIRONMENT_NAME == ENV_PRODUCTION:
    REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"] = {
        "anon": "100/day",
        "user": "1000/day",
    }


DJOSER = {
    ### USER CREATION ###
    "USER_CREATE_PASSWORD_RETYPE": True,
    "SEND_ACTIVATION_EMAIL": True,
    "ACTIVATION_URL": "activate/{uid}/{token}",
    "SEND_CONFIRMATION_EMAIL": True,
    ### USERNAME ###
    # # currently not supporting forgot username functionality
    # "USERNAME_RESET_CONFIRM_RETYPE": True,
    # "USERNAME_RESET_SHOW_EMAIL_NOT_FOUND": True,
    # "USERNAME_RESET_CONFIRM_URL": "username-reset-confirmation/{uid}/{token}",
    "SET_USERNAME_RETYPE": True,
    "USERNAME_CHANGED_EMAIL_CONFIRMATION": True,
    ### PASSWORD ###
    "PASSWORD_RESET_CONFIRM_RETYPE": True,
    "PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND": True,
    "PASSWORD_RESET_CONFIRM_URL": "password-reset-confirmation/{uid}/{token}",
    "SET_PASSWORD_RETYPE": True,
    "PASSWORD_CHANGED_EMAIL_CONFIRMATION": True,
    "LOGOUT_ON_PASSWORD_CHANGE": True,
    ### OTHER ###
    "SERIALIZERS": {
        "current_user": "users.serializers.UserSerializer",
        "user": "users.serializers.UserSerializer",
    },
    "TOKEN_MODEL": None,
    "HIDE_USERS": True,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": (
        timedelta(minutes=20) if ENVIRONMENT_NAME == ENV_LOCAL else timedelta(hours=1)
    ),
    "REFRESH_TOKEN_LIFETIME": (
        timedelta(hours=1) if ENVIRONMENT_NAME == ENV_LOCAL else timedelta(weeks=1)
    ),
}

SENTRY_ENABLED = env("SENTRY_ENABLED") and not TESTING
if SENTRY_ENABLED:
    sentry_sdk.init(
        dsn=env("SENTRY_DSN"),
        integrations=[DjangoIntegration()],
        environment=ENVIRONMENT_NAME,
        traces_sample_rate=1.0,
        send_default_pii=False,  # associate users to errors
    )

# https://docs.rollbar.com/docs/django
ROLLBAR_ENABLED = env("ROLLBAR_ENABLED") and not TESTING
ROLLBAR = {
    "enabled": ROLLBAR_ENABLED,
    "access_token": env("ROLLBAR_ACCESS_TOKEN"),
    "environment": ENVIRONMENT_NAME,
    "root": str(BASE_DIR),
    "branch": "main",
    "capture_email": True,
    "capture_username": True,
}
rollbar.init(**ROLLBAR)


# Custom settings
BIRTHDAY_FORMAT = "%m-%d"
MAX_EVENTS_PER_USER = 150
UNKNOWN_YEAR = 1000
UPCOMING_DAYS = 4
USER_COUNT_LIMIT = 100

# Cypress
CYPRESS_AUTH_SECRET = env("CYPRESS_AUTH_SECRET")
CYPRESS_QA_USER_EMAIL1 = env("CYPRESS_QA_USER_EMAIL1")
CYPRESS_QA_USER_EMAIL2 = env("CYPRESS_QA_USER_EMAIL2")
CYPRESS_QA_USER_PASSWORD = env("CYPRESS_QA_USER_PASSWORD")
