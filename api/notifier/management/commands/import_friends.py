import datetime

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from notifier.models import Friend


def import_friend(friend_data, user):
    name, bday = friend_data
    friend, created = Friend.objects.get_or_create(
        user=user, name=name, date_of_birth=datetime.date(*bday)
    )
    return friend, created


class Command(BaseCommand):
    help = "Import friends for a user."

    def add_arguments(self, parser):
        parser.add_argument("email", type=str, help="User email")
        parser.add_argument(
            "-f", "--filename", help="Friends file (defaults to '{email}_friends.csv')"
        )

    def handle(self, *args, **options):
        email = options["email"]
        filename = options["filename"]

        User = get_user_model()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise Exception(f"User {email} does not exist.")

        created_friends = user.add_friends_from_csv(filename=filename)

        for friend in created_friends:
            self.stdout.write(self.style.SUCCESS(f"{friend} created successfully."))
        self.stdout.write(
            self.style.SUCCESS(f"{len(created_friends)} friends created for {email}.")
        )
