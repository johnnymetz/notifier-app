from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from notifier.constants import BIRTHDAY_FORMAT, UNKNOWN_YEAR


class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friends")
    first_name = models.CharField("first name", max_length=30)
    # CharField's are set to an empty string if not provided;
    # never null (unless it is manually set)
    last_name = models.CharField("last name", max_length=150, null=True, blank=True)
    date_of_birth = models.DateField()

    class Meta:
        ordering = ["date_of_birth__month", "date_of_birth__day"]

    @property
    def age(self):
        if self.date_of_birth.year == UNKNOWN_YEAR:
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
        return self.date_of_birth.strftime(BIRTHDAY_FORMAT)

    def __str__(self):
        return (
            f"{self.first_name} {self.last_name}" if self.last_name else self.first_name
        )
