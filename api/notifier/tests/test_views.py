from django.urls import reverse

import pytest
from rest_framework import status

from notifier.tests.factories import UserFactory


@pytest.fixture
def access_token(client):
    url = reverse("token_obtain_pair")
    pw = "pass"
    u = UserFactory(password=pw)
    r = client.post(url, {"username": u.username, "password": pw})
    return r.data["access"]


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
def test_user_view(client, access_token):
    user_url = reverse("user-detail")
    headers = {"HTTP_AUTHORIZATION": "Bearer abc"}
    r = client.get(user_url, **headers)
    assert r.status_code == status.HTTP_401_UNAUTHORIZED
    headers = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}
    r = client.get(user_url, **headers)
    assert r.status_code == status.HTTP_200_OK
    assert "username" in r.data
    assert "email" in r.data
    assert "friends" in r.data
