import datetime

from django.utils import timezone

import pytest
import pytz

from notifier.tests.factories import FriendFactory


@pytest.mark.django_db
def test_friend_factory():
    FriendFactory()


@pytest.mark.freeze_time("2020-01-01")
def test_freeze_time_functionality():
    # print(timezone.now())  # UTC time
    # print(timezone.localdate())  # Local date
    # print(timezone.localtime())  # Local datetime
    assert datetime.datetime.now(tz=pytz.timezone("UTC")) == timezone.now()
    assert (
        datetime.datetime.now(tz=pytz.timezone("America/Los_Angeles"))
        == timezone.localtime()
    )
    assert datetime.datetime.now().date() == timezone.localdate(
        timezone=pytz.timezone("UTC")
    )
    assert datetime.datetime.now() == datetime.datetime.today()
