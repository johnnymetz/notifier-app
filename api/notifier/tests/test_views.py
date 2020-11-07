import datetime

from django.contrib.auth import get_user_model
from django.urls import reverse

import pytest
from rest_framework import status

from notifier.tests.factories import FriendFactory
from users.tests.factories import UserFactory

User = get_user_model()


@pytest.mark.django_db
def test_read_friend_list(client, token_headers):
    # TODO: this get request is not used and should probably be removed
    FriendFactory()
    FriendFactory()
    url = reverse("friend-list")
    r = client.get(url)
    assert r.status_code == status.HTTP_401_UNAUTHORIZED
    r = client.get(url, **token_headers)
    assert r.status_code == status.HTTP_200_OK
    assert r.data["count"] == 2
    assert len(r.data["results"]) == 2


@pytest.mark.django_db
def test_read_friend_detail(client, token_headers):
    u = User.objects.get()
    friend = FriendFactory(user=u)
    url = reverse("friend-detail", args=[friend.id])
    r = client.get(url)
    assert r.status_code == status.HTTP_401_UNAUTHORIZED
    r = client.get(url, **token_headers)
    assert r.status_code == status.HTTP_200_OK
    assert r.data["id"] == friend.id


@pytest.mark.django_db
def test_create_friend(client, token_headers):
    u = User.objects.get()
    url = reverse("friend-list")
    date = datetime.date(1994, 1, 24)
    data = {
        "name": "JJ Reddick",
        "date_of_birth": {"year": date.year, "month": date.month, "day": date.day},
    }
    r = client.post(url, data=data, content_type="application/json", **token_headers)
    assert r.status_code == status.HTTP_201_CREATED
    assert r.data["name"] == data["name"]
    assert r.data["user"] == u.id


@pytest.mark.django_db
def test_update_friend(client, token_headers):
    u = User.objects.get()
    friend = FriendFactory(user=u)
    url = reverse("friend-detail", args=[friend.id])
    date = datetime.date(1994, 1, 24)
    data = {
        "name": "JJ Reddick",
        "date_of_birth": {"year": date.year, "month": date.month, "day": date.day},
    }
    r = client.patch(url, data=data, content_type="application/json", **token_headers)
    assert r.status_code == status.HTTP_200_OK
    assert r.data["name"] == data["name"]
    assert r.data["user"] == u.id


@pytest.mark.django_db
def test_delete_friend(client, token_headers):
    u = User.objects.get()
    friend = FriendFactory(user=u)
    url = reverse("friend-detail", args=[friend.id])
    r = client.delete(url, **token_headers, content_type="application/json")
    assert r.status_code == status.HTTP_204_NO_CONTENT
    assert r.data is None
    assert not u.friends.exists()


@pytest.mark.django_db
def test_user_cant_read_or_delete_friend_of_another_user(client, token_headers):
    _ = User.objects.get()
    u = UserFactory()
    u_friend = FriendFactory(user=u)
    url = reverse("friend-detail", args=[u_friend.id])
    r = client.get(url, **token_headers)  # token belongs to _
    assert r.status_code == status.HTTP_403_FORBIDDEN
    r = client.delete(url, **token_headers)  # token belongs to _
    assert r.status_code == status.HTTP_403_FORBIDDEN
