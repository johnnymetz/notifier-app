import datetime
from zoneinfo import ZoneInfo

from django.db import connection, reset_queries
from django.utils import timezone

import pytest
from nplusone.core.exceptions import NPlusOneError

from notifier.models import Event
from notifier.tests.factories import EventFactory, UserFactory


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


@pytest.mark.django_db
def test_nplusone(settings):
    settings.DEBUG = True  # debug must be True to populate connection.queries
    u1 = UserFactory()
    for _ in range(100):
        EventFactory(user=u1)

    reset_queries()
    for e in Event.objects.all():
        with pytest.raises(NPlusOneError):
            assert e.user

    reset_queries()
    for e in Event.objects.select_related("user"):
        assert e.user
    assert len(connection.queries) == 1
