"""
Django settings for api project.

Generated by 'django-admin startproject' using Django 3.0.5.
"""

import os
from datetime import timedelta
from pathlib import Path

import rollbar

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


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
    "silk",
    "rest_framework",
    "djoser",
    "drf_yasg",
    # my apps
    "users.apps.UsersConfig",
    "notifier.apps.NotifierConfig",
]

MIDDLEWARE = [
    # rollbar Only404 should be first
    "rollbar.contrib.django.middleware.RollbarNotifierMiddlewareOnly404",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "silk.middleware.SilkyMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    # rollbar Excluding404 or the single middleware should be last
    "rollbar.contrib.django.middleware.RollbarNotifierMiddlewareExcluding404",

    # Reports all exceptions to Rollbar including 404s. Using the split 2 middlewares
    # allows you to skip reporting some 404s to Rollbar (not sure a use case here).
    # "rollbar.contrib.django.middleware.RollbarNotifierMiddleware",
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

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "postgres"),
        "USER": os.environ.get("DB_USERNAME", "postgres"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "postgres"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": os.environ.get("DB_PORT", 5432),
        "ATOMIC_REQUESTS": True,
    }
}

AUTH_USER_MODEL = "users.User"

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"


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


# django-silk
SILKY_PYTHON_PROFILER = True
SILKY_AUTHENTICATION = True
SILKY_AUTHORISATION = True
LOGIN_URL = "/backend/login/"


# django-templated-mail
DOMAIN = "localhost"
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
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],

    # Only works with rest_framework.test.APIClient + rest_framework.test.APIRequestFactory
    # "TEST_REQUEST_DEFAULT_FORMAT": "json",

    # Includes parsed POST variables in exception
    "EXCEPTION_HANDLER": "rollbar.contrib.django_rest_framework.post_exception_handler",
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
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(weeks=1),
}


# Custom settings
BIRTHDAY_FORMAT = "%m-%d"
MAX_EVENTS_PER_USER = 150
UNKNOWN_YEAR = 1000
UPCOMING_DAYS = 4
USER_COUNT_LIMIT = 100
