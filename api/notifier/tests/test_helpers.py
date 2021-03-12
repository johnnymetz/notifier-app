import datetime

import pytest

from notifier.helpers import sort_events_by_yearless_date_starting_at_today
from notifier.models import Event
from notifier.tests.factories import EventFactory


@pytest.mark.freeze_time("2020-06-01")
@pytest.mark.django_db
def test_sort_events_by_yearless_date_starting_at_today(settings):
    settings.TIME_ZONE = "UTC"
    event1 = EventFactory(annual_date=datetime.date(1990, 12, 31))
    event2 = EventFactory(annual_date=datetime.date(1991, 1, 1))
    event3 = EventFactory(annual_date=datetime.date(settings.UNKNOWN_YEAR, 12, 31))
    event4 = EventFactory(annual_date=datetime.date(settings.UNKNOWN_YEAR, 1, 1))
    event5 = EventFactory(annual_date=datetime.date(1990, 5, 31))
    event6 = EventFactory(annual_date=datetime.date(1991, 6, 1))
    event7 = EventFactory(annual_date=datetime.date(settings.UNKNOWN_YEAR, 5, 31))
    event8 = EventFactory(annual_date=datetime.date(settings.UNKNOWN_YEAR, 6, 1))
    assert sort_events_by_yearless_date_starting_at_today(Event.objects.all()) == [
        event6,
        event8,
        event1,
        event3,
        event2,
        event4,
        event5,
        event7,
    ]
