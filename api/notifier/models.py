from django.conf import settings
from django.db import models
from django.utils import timezone

from notifier.constants import BIRTHDAY_FORMAT, MAX_EVENTS_PER_USER, UNKNOWN_YEAR
from notifier.exceptions import NotifierException


class Event(models.Model):
    class Meta:
        ordering = ["annual_date__month", "annual_date__day"]

    class EventType(models.TextChoices):
        BIRTHDAY = "Birthday"
        HOLIDAY = "Holiday"
        OTHER = "Other"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="events"
    )
    name = models.CharField(max_length=255, unique=True)
    type = models.CharField(max_length=255, choices=EventType.choices)
    annual_date = models.DateField()

    @property
    def age(self):
        if self.annual_date.year == UNKNOWN_YEAR:
            return None
        today = timezone.localdate()
        return (
            today.year
            - self.annual_date.year
            - (
                (today.month, today.day)
                < (self.annual_date.month, self.annual_date.day)
            )
        )

    @property
    def annual_date_display(self):
        return self.annual_date.strftime(BIRTHDAY_FORMAT)

    def clean(self):
        if self.user_id and self.user.events.count() > MAX_EVENTS_PER_USER:
            raise NotifierException(f"{self.user} has reached the event limit")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
