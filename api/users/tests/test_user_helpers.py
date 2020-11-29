import datetime

import pytest

from notifier.constants import UNKNOWN_YEAR
from notifier.tests.factories import EventFactory
from users.tests.factories import UserFactory


@pytest.mark.freeze_time("2020-01-01")
@pytest.mark.django_db
def test_get_events_today(settings):
    settings.TIME_ZONE = "UTC"
    user = UserFactory()
    user2 = UserFactory()
    event1 = EventFactory(user=user, annual_date=datetime.date(1990, 1, 1))
    event2 = EventFactory(user=user, annual_date=datetime.date(UNKNOWN_YEAR, 1, 1))
    EventFactory(user=user, annual_date=datetime.date(1990, 1, 2))
    EventFactory(user=user, annual_date=datetime.date(UNKNOWN_YEAR, 1, 3))
    EventFactory(user=user2, annual_date=datetime.date(1990, 1, 1))
    events = user.get_events_today()
    assert event1 in events
    assert event2 in events
    assert events.count() == 2


@pytest.mark.freeze_time("2020-01-01")
@pytest.mark.django_db
def test_get_events_upcoming_at_month_start(settings):
    settings.TIME_ZONE = "UTC"
    user = UserFactory()
    user2 = UserFactory()
    event1 = EventFactory(user=user, annual_date=datetime.date(1990, 1, 2))
    event2 = EventFactory(user=user, annual_date=datetime.date(1990, 1, 5))
    event3 = EventFactory(user=user, annual_date=datetime.date(UNKNOWN_YEAR, 1, 2))
    event4 = EventFactory(user=user, annual_date=datetime.date(UNKNOWN_YEAR, 1, 5))
    EventFactory(user=user, annual_date=datetime.date(1990, 1, 1))
    EventFactory(user=user, annual_date=datetime.date(1990, 1, 6))
    EventFactory(user=user, annual_date=datetime.date(1989, 12, 31))
    EventFactory(user=user, annual_date=datetime.date(UNKNOWN_YEAR, 1, 1))
    EventFactory(user=user, annual_date=datetime.date(UNKNOWN_YEAR, 1, 6))
    EventFactory(user=user, annual_date=datetime.date(UNKNOWN_YEAR, 12, 31))
    EventFactory(user=user2, annual_date=datetime.date(1990, 1, 2))
    events = user.get_events_upcoming(days=5)
    assert event1 in events
    assert event2 in events
    assert event3 in events
    assert event4 in events
    assert len(events) == 4
    assert [f.date_display for f in events] == ["01-02", "01-02", "01-05", "01-05"]


@pytest.mark.freeze_time("2020-01-30")
@pytest.mark.django_db
def test_get_events_upcoming_at_month_end(settings):
    settings.TIME_ZONE = "UTC"
    user = UserFactory()
    event1 = EventFactory(user=user, annual_date=datetime.date(1990, 1, 31))
    event2 = EventFactory(user=user, annual_date=datetime.date(1990, 2, 1))
    event3 = EventFactory(user=user, annual_date=datetime.date(UNKNOWN_YEAR, 1, 31))
    event4 = EventFactory(user=user, annual_date=datetime.date(UNKNOWN_YEAR, 2, 2))
    EventFactory(user=user, annual_date=datetime.date(1990, 1, 30))
    EventFactory(user=user, annual_date=datetime.date(1990, 2, 10))
    EventFactory(user=user, annual_date=datetime.date(UNKNOWN_YEAR, 1, 30))
    EventFactory(user=user, annual_date=datetime.date(UNKNOWN_YEAR, 2, 10))
    events = user.get_events_upcoming(days=5)
    assert event1 in events
    assert event2 in events
    assert event3 in events
    assert event4 in events
    assert len(events) == 4
