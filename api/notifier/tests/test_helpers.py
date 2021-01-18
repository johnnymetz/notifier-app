import datetime

import pytest

from notifier.constants import UNKNOWN_YEAR
from notifier.helpers import sort_events_by_date_without_year
from notifier.models import Event
from notifier.tests.factories import EventFactory


@pytest.mark.skip(reason="TODO")
def test_sort_events_by_date_without_year():
    event1 = EventFactory(annual_date=datetime.date(1990, 12, 31))
    event2 = EventFactory(annual_date=datetime.date(1991, 1, 1))
    event3 = EventFactory(annual_date=datetime.date(UNKNOWN_YEAR, 12, 31))
    event4 = EventFactory(annual_date=datetime.date(UNKNOWN_YEAR, 1, 1))

    assert sort_events_by_date_without_year(Event) == [event1, event3, event2, event4]
