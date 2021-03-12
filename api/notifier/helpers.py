import datetime

from django.db.models import Q
from django.utils import timezone


def build_events_upcoming_query_filter(days: int) -> Q:
    date = timezone.localdate()

    # Build the list of month/day/year tuples.
    data = []
    for _ in range(days):
        date += datetime.timedelta(days=1)
        data.append((date.month, date.day, date.year))

    # Transform each into a Q object.
    filters = [
        Q(annual_date__month=month, annual_date__day=day, annual_date__year__lte=year)
        for month, day, year in data
    ]

    # Compose the Q objects together into a single query.
    query = Q()
    for f in filters:
        query |= f

    return query


def sort_events_by_yearless_date_starting_at_today(events):
    """
    Sort events so today is first and yesterday is last.
    Events on the same date are sorted by year in desc order.

    Today
    Today
    Tomorrow
    Tomorrow + 1
    ...
    Yesterday - 1
    Yesterday
    """
    today = timezone.localdate()
    today_date = (today.month, today.day)

    events_today = sorted(
        (e for e in events if (e.annual_date.month, e.annual_date.day) == today_date),
        key=lambda e: -e.annual_date.year,
    )
    events_later_this_year = sorted(
        (e for e in events if (e.annual_date.month, e.annual_date.day) > today_date),
        key=lambda e: (e.annual_date.month, e.annual_date.day, -e.annual_date.year),
    )
    events_earlier_this_year = sorted(
        (e for e in events if (e.annual_date.month, e.annual_date.day) < today_date),
        key=lambda e: (e.annual_date.month, e.annual_date.day, -e.annual_date.year),
    )

    return events_today + events_later_this_year + events_earlier_this_year


def add_one(x: int):
    """
    Test pytest doctest.

    >>> add_one(1)
    2
    >>> add_one(10)
    11
    >>> add_one(100)
    101
    """
    return x + 1
