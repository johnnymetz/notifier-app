import csv
import datetime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from notifier.constants import UNKNOWN_YEAR
from notifier.models import Friend

FRIENDS = [
    ("Dad", (1959, 3, 28)),
    ("Mom", (1960, 11, 26)),
    ("Aunt Rebecca", (UNKNOWN_YEAR, 4, 14)),
    ("Chris Fiore", (UNKNOWN_YEAR, 2, 19)),
]


def import_friend(friend_data, user):
    name, bday = friend_data
    friend, created = Friend.objects.get_or_create(
        user=user, name=name, date_of_birth=datetime.date(*bday),
    )
    return friend, created


class Command(BaseCommand):
    help = "Import friends for a user."

    def add_arguments(self, parser):
        parser.add_argument("username", help="Username to import friends to")
        parser.add_argument("-f", "--filename", help="Friends file")

    def handle(self, *args, **options):
        username = options["username"]
        filename = options["filename"]

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Exception(f"User {username} does not exist.")

        if not filename:
            filename = f"{username}_friends.csv"

        with open(filename) as f:
            count = 0
            csv_reader = csv.reader(f)
            for row in csv_reader:
                friend, created = Friend.objects.get_or_create(
                    user=user,
                    name=row[0],
                    date_of_birth=datetime.datetime.strptime(row[1], "%Y-%m-%d"),
                )
                if created:
                    count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f"{friend} created successfully.")
                    )

        self.stdout.write(
            self.style.SUCCESS(f"{count} friends created for {username}.")
        )
