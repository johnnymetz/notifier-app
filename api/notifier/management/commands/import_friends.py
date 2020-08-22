import datetime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from notifier.models import Friend
from notifier.user_helpers import add_friends_from_csv


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
        parser.add_argument(
            "-f",
            "--filename",
            help="Friends file (defaults to '{username}_friends.csv')",
        )

    def handle(self, *args, **options):
        username = options["username"]
        filename = options["filename"]

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Exception(f"User {username} does not exist.")

        created_friends = add_friends_from_csv(user=user, filename=filename)
        for friend in created_friends:
            self.stdout.write(self.style.SUCCESS(f"{friend} created successfully."))

        self.stdout.write(
            self.style.SUCCESS(
                f"{len(created_friends)} friends created for {username}."
            )
        )
