import datetime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from notifier.constants import UNKNOWN_YEAR
from notifier.models import Friend

FRIENDS = [
    ###
    ("Test", "0", (UNKNOWN_YEAR, 6, 30)),
    ("Test", "1", (UNKNOWN_YEAR, 7, 1)),
    ("Test", "2", (2000, 7, 2)),
    ("Test", "3", (1990, 7, 3)),
    ("Test", "4", (UNKNOWN_YEAR, 7, 4)),
    ("Test", "5", (UNKNOWN_YEAR, 7, 5)),
    ###
    ("Dad", None, (1959, 3, 28)),
    ("Mom", None, (1960, 11, 26)),
    ("Leah", None, (1995, 7, 17)),
    ("Allana", None, (1997, 9, 2)),
    ("Will", "Hewitt", (1999, 6, 25)),
    ("Graydon", "Hewitt", (1999, 6, 25)),
    ("Brendan", "Metz", (1997, 3, 12)),
    ("Uncle", "Paco", (1964, 6, 12)),
    ("Aunt", "Rebecca", (UNKNOWN_YEAR, 4, 14)),
    ("Chris", "Fiore", (UNKNOWN_YEAR, 2, 19)),
    ("Uncle", "Stan", (UNKNOWN_YEAR, 5, 4)),
    ("Sam", "Mayper", (UNKNOWN_YEAR, 12, 7)),
    ("Dan", "Mayper", (1995, 6, 28)),
    ("Elliot", "Yaghoobia", (UNKNOWN_YEAR, 8, 7)),
    ("James", "Theo", (1994, 6, 13)),
    ("Zack", "Haiman", (1993, 9, 7)),
    ("Gil", "Meshulam", (1994, 2, 5)),
    ("Ilana", "Fine", (1993, 9, 26)),
    ("Freda", "Chamberlain", (1993, 6, 9)),
    ("Talia", "Nassi", (1994, 9, 21)),
    ("Tamir", "Ram", (1993, 9, 28)),
    ("Kyle", "Pascual", (1991, 7, 7)),
    ("Eddie", "London", (1992, 7, 16)),
    ("Brad", "Friedman", (1990, 11, 11)),
    ("Josh", "Cera", (1991, 12, 6)),
    ("David", "Smyle", (1993, 4, 7)),
    ("Jordan", "Khorshidi", (UNKNOWN_YEAR, 7, 9)),
    ("Noah", "Lightman", (1995, 4, 28)),
    ("Josh", "Weiss", (1995, 3, 22)),
    ("Tony", "Yeoman", (1991, 7, 11)),
    ("Ian", "Toperczer", (1996, 5, 23)),
    ("Nick", "Galambos", (1995, 5, 25)),
    ("Jack", "Markavage", (1993, 9, 7)),
    ("Corey", "Fowler", (1990, 5, 21)),
    ("Cody", "Blick", (1993, 12, 5)),
    ("Zack", "Bailey", (1996, 10, 12)),
    ("Jake", "Suh", (1996, 3, 25)),
    ("Mike", "Perchak", (1990, 7, 6)),
]


def import_friend(friend_data, user):
    first_name, last_name, bday = friend_data
    friend, created = Friend.objects.get_or_create(
        user=user,
        first_name=first_name,
        last_name=last_name,
        date_of_birth=datetime.date(*bday),
    )
    return friend, created


class Command(BaseCommand):
    help = "Add friends for a user."

    def add_arguments(self, parser):
        parser.add_argument("username", type=str, help="Username to add friends to")

    def handle(self, *args, **options):
        username = options["username"]
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Exception(f"User {username} does not exist.")
        for friend_data in FRIENDS:
            friend, created = import_friend(friend_data, user)
            if created:
                self.stdout.write(self.style.SUCCESS(f"{friend} created successfully."))
