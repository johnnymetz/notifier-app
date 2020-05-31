from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from notifier.helpers import get_birthday_display


class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friends")
    first_name = models.CharField("first name", max_length=30, blank=True)
    last_name = models.CharField("last name", max_length=150, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    month = models.PositiveSmallIntegerField(null=True, blank=True)
    day = models.PositiveSmallIntegerField(null=True, blank=True)

    @property
    def name_display(self):
        return (
            f"{self.first_name} {self.last_name}" if self.last_name else self.first_name
        )

    @property
    def age(self):
        if not self.date_of_birth:
            return None
        today = timezone.localdate()
        return (
            today.year
            - self.date_of_birth.year
            - (
                (today.month, today.day)
                < (self.date_of_birth.month, self.date_of_birth.day)
            )
        )

    @property
    def birthday_display(self):
        return get_birthday_display(
            dt=self.date_of_birth, month=self.month, day=self.day
        )

    def clean(self):
        if not self.date_of_birth and not (self.month and self.day):
            raise ValidationError(
                "Both month and day are required if date_of_birth is None"
            )
        elif self.date_of_birth and (self.month or self.day):
            raise ValidationError(
                "Neither month nor day can be set if date_of_birth is provided"
            )

    def __str__(self):
        return self.name_display
