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
    is_subscribed = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: List[str] = []

    objects = UserManager()

    def __str__(self):
        return self.email

    # CUSTOM METHODS

    def get_events_today(self):
        today = timezone.localdate()
        return self.events.filter(
            Q(annual_date__month=today.month, annual_date__day=today.day)
        )

    def get_events_upcoming(self, days: int):
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
            Q(annual_date__month=month, annual_date__day=day)
            for month, day in monthdays
        ]

        # Compose the Q objects together into a single query.
        query = Q()
        for f in filters:
            query |= f

        events = self.events.filter(query)
        events_sorted = sorted(events, key=lambda x: x.date_display)
        return events_sorted

    def get_events_email_context(self) -> dict:
        events_today = self.get_events_today()
        events_upcoming = self.get_events_upcoming(days=5)
        context = {
            "today_display": timezone.localdate().strftime(BIRTHDAY_FORMAT),
            "events_today": events_today,
            "events_upcoming": events_upcoming,
        }
        return context

    def send_events_email(self, from_email: Optional[str] = None) -> None:
        """
        from_email defaults to DEFAULT_FROM_EMAIL,
        except when using gmail which defaults to EMAIL_HOST_USER
        """
        context = self.get_events_email_context()
        text_content = render_to_string("notifier/events-email.txt", context)
        html_content = render_to_string("notifier/events-email.html", context)
        self.email_user(
            subject="Today's Events",
            message=text_content,
            html_message=html_content,
            from_email=from_email,
        )

    def add_events_from_csv(self, filename: str) -> list:
        from notifier.models import Event

        if not filename:
            filename = f"{self.email}_events.csv"

        created_events = []
        with open(filename) as f:
            csv_reader = csv.reader(f)
            for row in csv_reader:
                event, created = Event.objects.get_or_create(
                    user=self,
                    name=row[0],
                    annual_date=datetime.datetime.strptime(row[1], "%Y-%m-%d").date(),
                )
                if created:
                    created_events.append(event)

        return created_events
