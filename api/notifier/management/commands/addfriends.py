import datetime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from notifier.models import Friend

FRIENDS = [
    ###
    ("Test", "0", (6, 30)),
    ("Test", "1", (7, 1)),
    ("Test", "2", (7, 2)),
    ("Test", "3", (7, 3)),
    ("Test", "4", (7, 4)),
    ("Test", "5", (7, 5)),
    ###
    ("Dad", None, datetime.date(1959, 3, 28)),
    ("Mom", None, datetime.date(1960, 11, 26)),
    ("Leah", None, datetime.date(1995, 7, 17)),
    ("Allana", None, datetime.date(1997, 9, 2)),
    ("Will", "Hewitt", datetime.date(1999, 6, 25)),
    ("Graydon", "Hewitt", datetime.date(1999, 6, 25)),
    ("Brendan", "Metz", datetime.date(1997, 3, 12)),
    ("Uncle", "Paco", datetime.date(1964, 6, 12)),
    ("Aunt", "Rebecca", (4, 14)),
    ("Chris", "Fiore", (2, 19)),
    ("Uncle", "Stan", (5, 4)),
    ("Sam", "Mayper", (12, 7)),
    ("Dan", "Mayper", datetime.date(1995, 6, 28)),
    ("Elliot", "Yaghoobia", (8, 7)),
    ("James", "Theo", datetime.date(1994, 6, 13)),
    ("Zack", "Haiman", datetime.date(1993, 9, 7)),
    ("Gil", "Meshulam", datetime.date(1994, 2, 5)),
    ("Ilana", "Fine", datetime.date(1993, 9, 26)),
    ("Freda", "Chamberlain", datetime.date(1993, 6, 9)),
    ("Talia", "Nassi", datetime.date(1994, 9, 21)),
    ("Tamir", "Ram", datetime.date(1993, 9, 28)),
    ("Kyle", "Pascual", datetime.date(1991, 7, 7)),
    ("Eddie", "London", datetime.date(1992, 7, 16)),
    ("Brad", "Friedman", datetime.date(1990, 11, 11)),
    ("Josh", "Cera", datetime.date(1991, 12, 6)),
    ("David", "Smyle", datetime.date(1993, 4, 7)),
    ("Jordan", "Khorshidi", (7, 9)),
    ("Noah", "Lightman", datetime.date(1995, 4, 28)),
    ("Josh", "Weiss", datetime.date(1995, 3, 22)),
    ("Tony", "Yeoman", datetime.date(1991, 7, 11)),
    ("Ian", "Toperczer", datetime.date(1996, 5, 23)),
    ("Nick", "Galambos", datetime.date(1995, 5, 25)),
    ("Jack", "Markavage", datetime.date(1993, 9, 7)),
    ("Corey", "Fowler", datetime.date(1990, 5, 21)),
    ("Cody", "Blick", datetime.date(1993, 12, 5)),
    ("Zack", "Bailey", datetime.date(1996, 10, 12)),
    ("Jake", "Suh", datetime.date(1996, 3, 25)),
    ("Mike", "Perchak", datetime.date(1990, 7, 6)),
]


def import_friend(friend_data, user):
    first_name, last_name, bday = friend_data
    if isinstance(bday, datetime.date):
        date_of_birth = bday
        month = None
        day = None
    else:
        date_of_birth = None
        month = bday[0]
        day = bday[1]
    friend, created = Friend.objects.get_or_create(
        user=user,
        first_name=first_name,
        last_name=last_name,
        date_of_birth=date_of_birth,
        month=month,
        day=day,
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
