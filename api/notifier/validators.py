import datetime

from django.core.exceptions import ValidationError
from django.utils import timezone

from notifier.constants import UNKNOWN_YEAR


def validate_annual_date(value: datetime.date):
    if value.year == UNKNOWN_YEAR:
        return
    elif value > timezone.localdate():
        raise ValidationError("Date of birth cannot be in the future")
