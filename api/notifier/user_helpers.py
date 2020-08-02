import datetime
import logging

from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone

from notifier.constants import BIRTHDAY_FORMAT

logger = logging.getLogger("django")


def get_friends_with_birthday_today(user: User):
    today = timezone.localdate()
    return user.friends.filter(
        Q(date_of_birth__month=today.month, date_of_birth__day=today.day)
    )


def get_friends_with_birthday_within(user: User, days: int):
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

    friends = user.friends.filter(query)
    friends_sorted = sorted(friends, key=lambda x: x.birthday_display)
    return friends_sorted


def get_birthday_email_context(user: User):
    friends_with_bday_today = get_friends_with_birthday_today(user)
    friends_with_bday_upcoming = get_friends_with_birthday_within(user, days=5)
    context = {
        "today_display": timezone.localdate().strftime(BIRTHDAY_FORMAT),
        "friends_with_bday_today": friends_with_bday_today,
        "friends_with_bday_upcoming": friends_with_bday_upcoming,
    }
    return context
