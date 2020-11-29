import csv

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Export events for a user."

    def add_arguments(self, parser):
        parser.add_argument("email", type=str, help="User email")

    def handle(self, *args, **options):
        email = options["email"]

        User = get_user_model()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise Exception(f"User {email} does not exist.")

        filename = f"{email}_events.csv"
        with open(filename, mode="w") as f:
            count = 0
            writer = csv.writer(f)
            for event in user.events.order_by("name").all():
                writer.writerow([event.name, event.annual_date])
                count += 1

        self.stdout.write(
            self.style.SUCCESS(f"{count} events export to {filename} successfully.")
        )
