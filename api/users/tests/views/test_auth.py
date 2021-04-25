import datetime

from django.urls import reverse
from django.utils import timezone

import pytest
from rest_framework import status

from users.tests.factories import TEST_PASSWORD, UserFactory


@pytest.mark.django_db()
def test_create_verify_refresh_jwt(client, freezer, settings):
    u = UserFactory(password=TEST_PASSWORD, is_active=False)

    create_url = reverse("jwt-create")
    r = client.post(create_url, {"username": u.email, "password": TEST_PASSWORD})
    assert r.status_code == status.HTTP_400_BAD_REQUEST
    r = client.post(create_url, {"email": u.email, "password": TEST_PASSWORD})
    assert r.status_code == status.HTTP_401_UNAUTHORIZED

    # create jwt
    u.is_active = True
    u.save()
    r = client.post(create_url, {"email": u.email, "password": TEST_PASSWORD})
    assert r.status_code == status.HTTP_200_OK
    assert "access" in r.data
    access_token = r.data["access"]
    refresh_token = r.data["refresh"]

    # verify jwt
    verify_url = reverse("jwt-verify")
    r = client.post(verify_url, {"token": access_token})
    assert r.status_code == status.HTTP_200_OK
    r = client.post(verify_url, {"token": "abc"})
    assert r.status_code == status.HTTP_401_UNAUTHORIZED

    # refresh jwt
    now = timezone.now()
    freezer.move_to(
        now
        + settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"]
        + datetime.timedelta(seconds=1)
    )
    r = client.post(verify_url, {"token": access_token})
    assert r.status_code == status.HTTP_401_UNAUTHORIZED
    refresh_url = reverse("jwt-refresh")
    r = client.post(refresh_url, {"refresh": refresh_token})
    assert r.status_code == status.HTTP_200_OK
    assert r.data["access"] != access_token


@pytest.mark.django_db()
def test_client_login(client):
    u = UserFactory(password=TEST_PASSWORD)
    is_logged_in = client.login(email=u.email, password="bad")
    assert not is_logged_in
    is_logged_in = client.login(email=u.email, password=TEST_PASSWORD)
    assert is_logged_in
