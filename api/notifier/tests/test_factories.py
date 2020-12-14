import datetime
from zoneinfo import ZoneInfo

from django.utils import timezone

import pytest

from notifier.tests.factories import EventFactory


@pytest.mark.django_db
def test_event_factory():
    EventFactory()


@pytest.mark.freeze_time("2020-01-01")
def test_freeze_time_functionality():
    # print(timezone.now())  # UTC time
    # print(timezone.localdate())  # Local date
    # print(timezone.localtime())  # Local datetime
    assert datetime.datetime.now(tz=ZoneInfo("UTC")) == timezone.now()
    assert (
        datetime.datetime.now(tz=ZoneInfo("America/Los_Angeles"))
        == timezone.localtime()
    )
    assert datetime.datetime.now().date() == timezone.localdate(
        timezone=ZoneInfo("UTC")
    )
    assert datetime.datetime.now() == datetime.datetime.today()
