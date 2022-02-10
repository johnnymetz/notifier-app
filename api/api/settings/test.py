from .base import *

SECRET_KEY = "12345"  # nosec
DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

AUTH_PASSWORD_VALIDATORS = []

PASSWORD_HASHERS = ("django.contrib.auth.hashers.MD5PasswordHasher",)

# N+1
INSTALLED_APPS.append("nplusone.ext.django")
MIDDLEWARE.insert(0, "nplusone.ext.django.NPlusOneMiddleware")
NPLUSONE_RAISE = True

# silk
MIDDLEWARE.remove("silk.middleware.SilkyMiddleware")
