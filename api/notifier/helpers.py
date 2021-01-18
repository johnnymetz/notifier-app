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
        Q(
            annual_date__month=month,
            annual_date__day=day,
            annual_date__year__lte=year,
        )
        for month, day, year in data
    ]

    # Compose the Q objects together into a single query.
    query = Q()
    for f in filters:
        query |= f

    return query


def sort_events_by_date_without_year(events):
    """Get upcoming events. Sort by date, not including the year."""
    return events
