from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from notifier.constants import BIRTHDAY_FORMAT, MAX_FRIENDS_PER_USER, UNKNOWN_YEAR
from notifier.exceptions import NotifierException
from notifier.validators import validate_date_of_birth


class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friends")
    name = models.CharField(max_length=255, unique=True)
    date_of_birth = models.DateField(validators=[validate_date_of_birth])

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

    def clean(self):
        if self.user_id and self.user.friends.count() > MAX_FRIENDS_PER_USER:
            raise NotifierException(f"{self.user} has reached the friend limit")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
