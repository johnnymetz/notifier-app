import datetime

from django.urls import reverse

import pytest
from rest_framework import status

from notifier.models import Event
from notifier.tests.factories import EventFactory
from users.models import User
from users.tests.factories import UserFactory


@pytest.mark.django_db()
def test_read_event_list(client, token_headers):
    EventFactory()
    EventFactory()
    url = reverse("event-list")
    r = client.get(url)
    assert r.status_code == status.HTTP_401_UNAUTHORIZED
    r = client.get(url, **token_headers)
    assert r.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.django_db()
def test_read_event_detail(client, token_headers):
    u = User.objects.get()
    event = EventFactory(user=u)
    url = reverse("event-detail", args=[event.id])
    r = client.get(url)
    assert r.status_code == status.HTTP_401_UNAUTHORIZED
    r = client.get(url, **token_headers)
    assert r.status_code == status.HTTP_200_OK
    assert r.data["id"] == event.id


@pytest.mark.django_db()
def test_create_event(client, token_headers):
    u = User.objects.get()
    url = reverse("event-list")
    date = datetime.date(1994, 1, 24)
    data = {
        "name": "JJ Reddick",
        "annual_date": {"year": date.year, "month": date.month, "day": date.day},
        "type": "Birthday",
    }
    r = client.post(url, data=data, content_type="application/json", **token_headers)
    assert r.status_code == status.HTTP_201_CREATED
    assert r.data["name"] == data["name"]
    assert r.data["user"] == u.id


@pytest.mark.django_db()
def test_update_event(client, token_headers):
    u = User.objects.get()
    event = EventFactory(user=u)
    url = reverse("event-detail", args=[event.id])

    name = "Something else"
    date = datetime.date(1994, 1, 1)
    _type = Event.EventType.OTHER
    assert event.name != name
    assert event.annual_date != date
    assert event.type != _type

    data = {
        "name": name,
        "annual_date": {"year": date.year, "month": date.month, "day": date.day},
        "type": _type.value,
    }
    r = client.patch(url, data=data, content_type="application/json", **token_headers)
    assert r.status_code == status.HTTP_200_OK
    assert r.data["name"] == name
    assert r.data["type"] == _type.value
    assert r.data["user"] == u.id

    event.refresh_from_db()
    assert event.name == name
    assert event.annual_date == date
    assert event.type == _type


@pytest.mark.django_db()
def test_delete_event(client, token_headers):
    u = User.objects.get()
    event = EventFactory(user=u)
    url = reverse("event-detail", args=[event.id])
    r = client.delete(url, **token_headers, content_type="application/json")
    assert r.status_code == status.HTTP_204_NO_CONTENT
    assert r.data is None
    assert not u.events.exists()


@pytest.mark.django_db()
def test_user_cant_read_or_delete_event_of_another_user(client, token_headers):
    _ = User.objects.get()
    u = UserFactory()
    u_event = EventFactory(user=u)
    url = reverse("event-detail", args=[u_event.id])
    r = client.get(url, **token_headers)  # token belongs to _
    assert r.status_code == status.HTTP_403_FORBIDDEN
    r = client.delete(url, **token_headers)  # token belongs to _
    assert r.status_code == status.HTTP_403_FORBIDDEN
