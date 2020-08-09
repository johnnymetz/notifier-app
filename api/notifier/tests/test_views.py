import datetime

from django.contrib.auth.models import User
from django.urls import reverse

import pytest
from rest_framework import status

from notifier.tests.factories import FriendFactory, UserFactory


@pytest.fixture
def token_headers(client):
    url = reverse("token_obtain_pair")
    pw = "pass"
    u = UserFactory(password=pw)
    r = client.post(url, {"username": u.username, "password": pw})
    access_token = r.data["access"]
    headers = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}
    return headers


@pytest.mark.django_db
def test_jwt(client):
    url = reverse("token_obtain_pair")
    pw = "pass"
    u = UserFactory(password=pw)
    u.is_active = False
    u.save()
    r = client.post(url, {"email": u.email, "password": pw})
    assert r.status_code == status.HTTP_400_BAD_REQUEST
    r = client.post(url, {"username": u.username, "password": pw})
    assert r.status_code == status.HTTP_401_UNAUTHORIZED

    u.is_active = True
    u.save()
    r = client.post(url, {"username": u.username, "password": pw})
    assert r.status_code == status.HTTP_200_OK
    assert "access" in r.data
    token = r.data["access"]

    verification_url = reverse("token_verify")
    r = client.post(verification_url, {"token": token})
    assert r.status_code == status.HTTP_200_OK
    r = client.post(verification_url, {"token": "abc"})
    assert r.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_client_login(client):
    pw = "pass"
    u = UserFactory(password=pw)
    is_logged_in = client.login(username=u.username, password="bad")
    assert not is_logged_in
    is_logged_in = client.login(username=u.username, password=pw)
    assert is_logged_in


@pytest.mark.django_db
def test_unauthenticated_read_friend_list(client):
    u = UserFactory()
    FriendFactory(user=u)
    url = reverse("friend-list")
    r = client.get(url)
    assert r.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_unauthenticated_read_friend_detail(client):
    u = UserFactory()
    friend = FriendFactory(user=u)
    url = reverse("friend-detail", args=[friend.id])
    r = client.get(url)
    assert r.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_read_friend_detail(client, token_headers):
    u = User.objects.get()
    friend = FriendFactory(user=u)
    url = reverse("friend-detail", args=[friend.id])
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


@pytest.mark.django_db
def test_unauthenticated_read_user_detail(client):
    url = reverse("user-detail")
    r = client.get(url)
    assert r.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_read_user_detail(client, token_headers):
    u = User.objects.get()
    url = reverse("user-detail")
    r = client.get(url, **token_headers)
    assert r.status_code == status.HTTP_200_OK
    assert r.data["id"] == u.id


# test creating new user (post)
# test updating user (patch)
# test deactivating user (is_active=False)
