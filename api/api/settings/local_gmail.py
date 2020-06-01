from .base import *
from .local import *

# Email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get("GMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("GMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True
