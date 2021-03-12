import datetime

from django.db import DataError

import pytest

from notifier.tests.factories import EventFactory
from users.tests.factories import UserFactory


@pytest.mark.freeze_time("2020-01-01")
@pytest.mark.django_db
def test_get_events_today(settings):
    settings.TIME_ZONE = "UTC"
    user = UserFactory()
    user2 = UserFactory()
    event1 = EventFactory(user=user, annual_date=datetime.date(1990, 1, 1))
    event2 = EventFactory(
        user=user, annual_date=datetime.date(settings.UNKNOWN_YEAR, 1, 1)
    )
    EventFactory(user=user, annual_date=datetime.date(1990, 1, 2))
    EventFactory(user=user, annual_date=datetime.date(settings.UNKNOWN_YEAR, 1, 2))
    EventFactory(user=user, annual_date=datetime.date(1989, 12, 31))
    EventFactory(user=user, annual_date=datetime.date(2021, 1, 1))
    EventFactory(user=user, annual_date=datetime.date(2030, 1, 1))
    EventFactory(user=user2, annual_date=datetime.date(1990, 1, 1))
    assert set(user.get_events_today()) == {event1, event2}


@pytest.mark.freeze_time("2020-01-01")
@pytest.mark.django_db
def test_get_events_upcoming_at_month_start(settings):
    settings.TIME_ZONE = "UTC"
    user = UserFactory()
    user2 = UserFactory()
    event1 = EventFactory(user=user, annual_date=datetime.date(1990, 1, 2))
    event2 = EventFactory(user=user, annual_date=datetime.date(1990, 1, 5))
    event3 = EventFactory(
        user=user, annual_date=datetime.date(settings.UNKNOWN_YEAR, 1, 2)
    )
    event4 = EventFactory(
        user=user, annual_date=datetime.date(settings.UNKNOWN_YEAR, 1, 5)
    )
    EventFactory(user=user, annual_date=datetime.date(1990, 1, 1))
    EventFactory(user=user, annual_date=datetime.date(1990, 1, 6))
    EventFactory(user=user, annual_date=datetime.date(1989, 12, 31))
    EventFactory(user=user, annual_date=datetime.date(settings.UNKNOWN_YEAR, 1, 1))
    EventFactory(user=user, annual_date=datetime.date(settings.UNKNOWN_YEAR, 1, 6))
    EventFactory(user=user, annual_date=datetime.date(settings.UNKNOWN_YEAR, 12, 31))
    EventFactory(user=user, annual_date=datetime.date(2021, 1, 2))
    EventFactory(user=user, annual_date=datetime.date(2030, 1, 3))
    EventFactory(user=user2, annual_date=datetime.date(1990, 1, 2))
    assert list(user.get_events_upcoming()) == [event1, event3, event2, event4]


@pytest.mark.freeze_time("2020-01-30")
@pytest.mark.django_db
def test_get_events_upcoming_at_month_end(settings):
    settings.TIME_ZONE = "UTC"
    user = UserFactory()
    event1 = EventFactory(user=user, annual_date=datetime.date(1990, 1, 31))
    event2 = EventFactory(user=user, annual_date=datetime.date(1990, 2, 1))
    event3 = EventFactory(
        user=user, annual_date=datetime.date(settings.UNKNOWN_YEAR, 1, 31)
    )
    event4 = EventFactory(
        user=user, annual_date=datetime.date(settings.UNKNOWN_YEAR, 2, 2)
    )
    EventFactory(user=user, annual_date=datetime.date(1990, 1, 30))
    EventFactory(user=user, annual_date=datetime.date(1990, 2, 10))
    EventFactory(user=user, annual_date=datetime.date(settings.UNKNOWN_YEAR, 1, 30))
    EventFactory(user=user, annual_date=datetime.date(settings.UNKNOWN_YEAR, 2, 10))
    assert list(user.get_events_upcoming()) == [event1, event3, event2, event4]


@pytest.mark.freeze_time("2020-12-30")
@pytest.mark.django_db
def test_get_events_upcoming_at_year_end(settings):
    settings.TIME_ZONE = "UTC"
    user = UserFactory()
    event1 = EventFactory(user=user, annual_date=datetime.date(1990, 12, 31))
    event2 = EventFactory(user=user, annual_date=datetime.date(1991, 1, 1))
    event3 = EventFactory(
        user=user, annual_date=datetime.date(settings.UNKNOWN_YEAR, 12, 31)
    )
    event4 = EventFactory(
        user=user, annual_date=datetime.date(settings.UNKNOWN_YEAR, 1, 1)
    )
    EventFactory(user=user, annual_date=datetime.date(1990, 12, 30))
    EventFactory(user=user, annual_date=datetime.date(1991, 1, 10))
    EventFactory(user=user, annual_date=datetime.date(settings.UNKNOWN_YEAR, 12, 30))
    EventFactory(user=user, annual_date=datetime.date(settings.UNKNOWN_YEAR, 1, 10))
    assert list(user.get_events_upcoming()) == [event1, event3, event2, event4]


@pytest.mark.django_db
def test_exceed_user_count_limit(settings):
    assert settings.USER_COUNT_LIMIT
    for _ in range(settings.USER_COUNT_LIMIT):
        UserFactory()
    with pytest.raises(DataError, match="User count limit exceeded"):
        UserFactory()
