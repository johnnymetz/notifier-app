from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Send birthday notifier email to a user."

    def add_arguments(self, parser):
        parser.add_argument("email", type=str, help="User email")

    def handle(self, *args, **options):
        email = options["email"]

        User = get_user_model()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise Exception(f"User {email} does not exist.")

        user.send_birthday_notifier_email()

        self.stdout.write(self.style.SUCCESS(f"Email to {user} successfully sent."))
