import datetime
from unittest.mock import create_autospec

import pytest
from rest_framework.request import Request

from notifier.serializers import EventSerializer
from notifier.tests.factories import EventFactory
from users.tests.factories import UserFactory


@pytest.mark.django_db()
def test_read_event_fields():
    event = EventFactory()
    data = EventSerializer(event).data
    assert data["id"] == event.id
    assert data["user"] == event.user.id
    assert data["name"] == event.name
    assert data["annual_date"]["year"] == event.annual_date.year
    assert data["annual_date"]["month"] == event.annual_date.month
    assert data["annual_date"]["day"] == event.annual_date.day
    assert data["type"] == event.type
    assert data["age"] == event.age


@pytest.mark.django_db()
def test_read_event_fields_without_year(settings):
    event = EventFactory()
    event.annual_date = event.annual_date.replace(year=settings.UNKNOWN_YEAR)
    data = EventSerializer(event).data
    assert data["id"] == event.id
    assert data["user"] == event.user.id
    assert data["name"] == event.name
    assert data["annual_date"]["year"] is None
    assert data["annual_date"]["month"] == event.annual_date.month
    assert data["annual_date"]["day"] == event.annual_date.day
    assert data["type"] == event.type
    assert data["age"] == event.age


@pytest.mark.django_db()
def test_create_event():
    u = UserFactory()
    date = datetime.date(1994, 1, 24)
    data = {
        "name": "JJ Reddick",
        "annual_date": {"year": date.year, "month": date.month, "day": date.day},
        "type": "Birthday",
    }
    request = create_autospec(Request, spec_set=True, instance=True, user=u)
    serializer = EventSerializer(data=data, context={"request": request})
    assert serializer.is_valid(raise_exception=True)
    event = serializer.save()
    assert event.name == data["name"]
    assert event.annual_date == date
    assert event.user == u


@pytest.mark.django_db()
def test_update_event():
    u = UserFactory()
    event = EventFactory(user=u)
    date = datetime.date(1994, 1, 24)
    data = {
        "name": "JJ Reddick",
        "annual_date": {"year": date.year, "month": date.month, "day": date.day},
        "type": "Birthday",
    }
    serializer = EventSerializer(event, data=data)
    assert serializer.is_valid(raise_exception=True)
    event = serializer.save()
    assert event.name == data["name"]
    assert event.annual_date == date
    assert event.user == u


@pytest.mark.django_db()
def test_update_event_without_year(settings):
    u = UserFactory()
    event = EventFactory(user=u)
    date = datetime.date(1994, 1, 24)
    data = {
        "name": "JJ Reddick",
        "annual_date": {"month": date.month, "day": date.day},
        "type": "Birthday",
    }
    serializer = EventSerializer(event, data=data)
    assert serializer.is_valid(raise_exception=True)
    event = serializer.save()
    assert event.name == data["name"]
    assert event.annual_date == datetime.date(
        settings.UNKNOWN_YEAR, date.month, date.day
    )
    assert event.user == u
