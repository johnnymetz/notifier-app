import csv
import datetime
import random
from typing import Optional

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import DataError, models
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from notifier.helpers import build_events_upcoming_query_filter
from users.managers import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    is_subscribed = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []

    objects = UserManager()

    def __str__(self):
        return self.email

    # CUSTOM METHODS

    # TODO: type hint qs return value, also figure out how to use
    #  qa[Event] type hint even though Event isn't defined yet
    def get_events_today(self):
        """
        Get events today in history, including past events but excluding future events.
        """
        today = timezone.localdate()
        return self.events.filter(
            annual_date__month=today.month,
            annual_date__day=today.day,
            annual_date__year__lte=today.year,
        )

    def get_events_upcoming(self, days: int = settings.UPCOMING_DAYS):
        """Get upcoming events. Sort by date, not including the year"""
        from notifier.helpers import sort_events_by_yearless_date_starting_at_today

        query_filter = build_events_upcoming_query_filter(days=days)
        events = self.events.filter(query_filter)
        return sort_events_by_yearless_date_starting_at_today(events)

    def get_events_email_context(self) -> dict:
        events_today = self.get_events_today()
        events_upcoming = self.get_events_upcoming()
        return {
            "today_display": timezone.localdate().strftime(settings.BIRTHDAY_FORMAT),
            "events_today": events_today,
            "events_upcoming": events_upcoming,
        }

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

    # TODO: same type hint thing as above
    def add_events_from_csv(self, filename: str) -> list:
        from notifier.models import Event

        if not filename:
            filename = f"{self.email}_events.csv"

        created_events = []
        with open(filename) as f:
            csv_reader = csv.reader(f)
            rows = list(csv_reader)

            # Shuffle the rows so we known our sorting logic works correctly
            random.shuffle(rows)

            for row in rows:
                name, annual_date_str, _type = row
                event, created = Event.objects.get_or_create(
                    user=self,
                    name=name,
                    annual_date=datetime.datetime.strptime(
                        annual_date_str, "%Y-%m-%d"
                    ).date(),
                    type=_type,
                )
                if created:
                    created_events.append(event)

        return created_events

    def save(self, *args, **kwargs):
        if (self.__class__.objects.count() + 1) > settings.USER_COUNT_LIMIT:
            raise DataError("User count limit exceeded")

        super().save(*args, **kwargs)
