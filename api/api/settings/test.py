from .base import *

SECRET_KEY = "12345"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

AUTH_PASSWORD_VALIDATORS = []

PASSWORD_HASHERS = ("django.contrib.auth.hashers.MD5PasswordHasher",)

# django-templated-mail
DOMAIN = "localhost"
