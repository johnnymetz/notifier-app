import datetime
import logging
from typing import Optional

from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils import timezone

from notifier.exceptions import NotifierException

logger = logging.getLogger("django")


def get_birthday_display(dt: datetime.date):
    return dt.strftime("%m/%d")


def get_friends_with_birthday_today(user: User):
    today = timezone.localdate()
    return user.friends.filter(
        Q(date_of_birth__month=today.month, date_of_birth__day=today.day)
    )


def get_friends_with_birthday_within(user: User, days):
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
        "today_display": get_birthday_display(timezone.localdate()),
        "friends_with_bday_today": friends_with_bday_today,
        "friends_with_bday_upcoming": friends_with_bday_upcoming,
    }
    return context


def send_notifier_email(
    subject: str,
    text_content: str,
    html_content: str,
    to: str,
    from_email: Optional[str] = None,
):
    """
    from_email defaults to EMAIL_HOST_USER when using Gmail
    """
    msg = EmailMultiAlternatives(
        subject=subject, body=text_content, from_email=from_email, to=[to]
    )
    msg.attach_alternative(html_content, "text/html")
    sent = msg.send()
    return sent


def send_birthday_notifier_email_to_user(user: User, from_email: Optional[str] = None):
    if not user.email:
        raise NotifierException(f"{user} must provide an email.")
    context = get_birthday_email_context(user)
    text_content = render_to_string("notifier/birthdays-email.txt", context)
    html_content = render_to_string("notifier/birthdays-email.html", context)
    sent = send_notifier_email(
        subject="Today's Birthdays",
        text_content=text_content,
        html_content=html_content,
        to=user.email,
        from_email=from_email,
    )
    return sent


# def send_birthday_notifier_email_to_all_users():
#     emails_sent = 0
#     users = User.objects.all()
#     for user in users:
#         # logger.debug(f"Sending email to {user}...")
#         try:
#             sent = send_birthday_notifier_email_to_user(user)
#             if sent:
#                 # logger.debug(f"Email to {user} successfully sent.")
#                 emails_sent += 1
#         except NotifierException as e:
#             logger.error(f"Error sending email to {user}: {e}")
#     logger.info(f"Number of email successfully sent: {emails_sent}")
#     return emails_sent
