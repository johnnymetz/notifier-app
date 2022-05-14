from django.core.exceptions import ImproperlyConfigured

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
    "formatters": {
        "rich": {
            "datefmt": "[%X]",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
        },
        "rich": {
            "class": "rich.logging.RichHandler",
            "formatter": "rich",
            "level": "DEBUG",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["rich"],
        },
        "api.metrics": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}


REDIS_URL = os.environ.get("REDIS_URL")
REDIS_MAX_CONNECTIONS_PER_CACHE = 2
CACHE_DB_LOCATIONS = {"default": 0, "another": 1}


def redis_or_locmem_cache(location: str):
    """Return cache configuration for the given cache location."""

    database = CACHE_DB_LOCATIONS.get(location)

    if database is None or database < 0 or database > 15:
        # https://www.digitalocean.com/community/cheatsheets/how-to-manage-redis-databases-and-keys
        raise ImproperlyConfigured(
            f"Invalid Redis database: {database} (must be between 0 and 15, inclusive)"
        )

    if redis_url := REDIS_URL:
        # TODO: look into if each cache uses a different connection pool or shares the same one
        connection_pool_kwargs = {"max_connections": REDIS_MAX_CONNECTIONS_PER_CACHE}

        return {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": f"{redis_url}/{database}",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                "CONNECTION_POOL_KWARGS": connection_pool_kwargs,
            },
        }

    return {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": location,
    }


CACHES = {location: redis_or_locmem_cache(location) for location in CACHE_DB_LOCATIONS}


# https://docs.rollbar.com/docs/django
ROLLBAR = {
    "enabled": os.environ.get("ROLLBAR_ENABLED", "").lower() == "true",
    "access_token": os.environ.get("ROLLBAR_ACCESS_TOKEN"),
    "environment": "development",
    "root": str(BASE_DIR),
    "branch": "main",
    "capture_email": True,
    "capture_username": True,
}
rollbar.init(**ROLLBAR)
