from django.core.management.base import BaseCommand
from django.db import transaction

from users.models import User


class Command(BaseCommand):
    help = "Import events for a user."  # noqa

    def add_arguments(self, parser):
        parser.add_argument("email", type=str, help="User email")
        parser.add_argument(
            "-f", "--filename", help="Events file (defaults to '{email}_events.csv')"
        )

    @transaction.atomic
    def handle(self, *args, **options):
        email = options["email"]
        filename = options["filename"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise Exception(f"User {email} does not exist.")

        created_events = user.add_events_from_csv(filename=filename)

        for event in created_events:
            self.stdout.write(self.style.SUCCESS(f"{event} created successfully."))
        self.stdout.write(
            self.style.SUCCESS(f"{len(created_events)} events created for {email}.")
        )
