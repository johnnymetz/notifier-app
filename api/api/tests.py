from django.urls import reverse

import pytest
from rest_framework import status


def test_welcome_view(client):
    url = reverse("welcome")
    r = client.get(url)
    assert r.status_code == status.HTTP_200_OK


def test_anon_throttle_rate(client):
    rate = 5
    url = reverse("welcome")
    for _ in range(rate):
        r = client.get(url)
        assert r.status_code == status.HTTP_200_OK
    r = client.get(url)
    assert r.status_code == status.HTTP_429_TOO_MANY_REQUESTS


@pytest.mark.django_db
def test_user_throttle_rate(client, token_headers):
    rate = 100
    url = reverse("user-detail")
    for _ in range(rate):
        r = client.get(url, **token_headers)
        assert r.status_code == status.HTTP_200_OK
    r = client.get(url, **token_headers)
    assert r.status_code == status.HTTP_429_TOO_MANY_REQUESTS
