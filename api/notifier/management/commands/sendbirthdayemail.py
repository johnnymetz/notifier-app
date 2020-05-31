from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from notifier.helpers import send_birthday_notifier_email_to_user


class Command(BaseCommand):
    help = "Send birthday notifier email to a user."

    def add_arguments(self, parser):
        parser.add_argument("username", type=str, help="Username to add friends to")

    def handle(self, *args, **options):
        username = options["username"]
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Exception(f"User {username} does not exist.")
        sent = send_birthday_notifier_email_to_user(user=user)
        if sent:
            self.stdout.write(self.style.SUCCESS(f"Email to {user} successfully sent."))
