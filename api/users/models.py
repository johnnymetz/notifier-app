import csv
import datetime
import logging
from typing import List, Optional

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from notifier.constants import BIRTHDAY_FORMAT
from users.managers import UserManager

logger = logging.getLogger("django")


class User(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: List[str] = []

    objects = UserManager()

    def __str__(self):
        return self.email

    # CUSTOM METHODS

    def get_friends_with_birthday_today(self):
        today = timezone.localdate()
        return self.friends.filter(
            Q(date_of_birth__month=today.month, date_of_birth__day=today.day)
        )

    def get_friends_with_birthday_within(self, days: int):
        today = timezone.localdate()
        later = today + datetime.timedelta(days=days)

        # Build the list of month/day tuples.
        monthdays = []
        counter = today + datetime.timedelta(days=1)
        while counter < later:
            monthdays.append((counter.month, counter.day))
            counter += datetime.timedelta(days=1)

        # Transform each into a Q object.
        filters = [
            Q(date_of_birth__month=month, date_of_birth__day=day)
            for month, day in monthdays
        ]

        # Compose the Q objects together into a single query.
        query = Q()
        for f in filters:
            query |= f

        friends = self.friends.filter(query)
        friends_sorted = sorted(friends, key=lambda x: x.birthday_display)
        return friends_sorted

    def get_birthday_email_context(self) -> dict:
        friends_with_bday_today = self.get_friends_with_birthday_today()
        friends_with_bday_upcoming = self.get_friends_with_birthday_within(days=5)
        context = {
            "today_display": timezone.localdate().strftime(BIRTHDAY_FORMAT),
            "friends_with_bday_today": friends_with_bday_today,
            "friends_with_bday_upcoming": friends_with_bday_upcoming,
        }
        return context

    def send_birthday_notifier_email(self, from_email: Optional[str] = None) -> None:
        """
        from_email defaults to DEFAULT_FROM_EMAIL,
        except when using gmail which defaults to EMAIL_HOST_USER
        """
        context = self.get_birthday_email_context()
        text_content = render_to_string("notifier/birthdays-email.txt", context)
        html_content = render_to_string("notifier/birthdays-email.html", context)
        self.email_user(
            subject="Today's Birthdays",
            message=text_content,
            html_message=html_content,
            from_email=from_email,
        )

    def add_friends_from_csv(self, filename: str) -> list:
        from notifier.models import Friend

        if not filename:
            filename = f"{self.email}_friends.csv"

        created_friends = []
        with open(filename) as f:
            csv_reader = csv.reader(f)
            for row in csv_reader:
                friend, created = Friend.objects.get_or_create(
                    user=self,
                    name=row[0],
                    date_of_birth=datetime.datetime.strptime(row[1], "%Y-%m-%d"),
                )
                if created:
                    created_friends.append(friend)

        return created_friends
