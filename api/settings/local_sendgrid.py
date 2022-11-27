from .local import *

# Email
EMAIL_BACKEND = "anymail.backends.sendgrid.EmailBackend"
DEFAULT_FROM_EMAIL = os.environ["DEFAULT_FROM_EMAIL"]
ANYMAIL = {"SENDGRID_API_KEY": os.environ["SENDGRID_API_KEY"]}
