import csv

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Export friends for a user."

    def add_arguments(self, parser):
        parser.add_argument("username", help="Username to export friends from")

    def handle(self, *args, **options):
        username = options["username"]
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Exception(f"User {username} does not exist.")

        filename = f"{username}_friends.csv"
        with open(filename, mode="w") as f:
            count = 0
            writer = csv.writer(f)
            for friend in user.friends.order_by("name").all():
                writer.writerow([friend.name, friend.date_of_birth])
                count += 1

        self.stdout.write(
            self.style.SUCCESS(f"{count} friends export to {filename} successfully.")
        )
