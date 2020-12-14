from django.urls import reverse

import pytest
from rest_framework import status


def test_welcome_view(client):
    url = reverse("welcome")
    r = client.get(url)
    assert r.status_code == status.HTTP_200_OK


@pytest.fixture
def enable_throttle_rates(settings):
    settings.REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"] = {
        "anon": "10/day",
        "user": "20/day",
    }


def test_anon_throttle_rate(client, settings, enable_throttle_rates):
    rate = int(
        settings.REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"]["anon"].removesuffix("/day")
    )
    url = reverse("welcome")
    for _ in range(rate):
        r = client.get(url)
        assert r.status_code == status.HTTP_200_OK
    r = client.get(url)
    assert r.status_code == status.HTTP_429_TOO_MANY_REQUESTS


@pytest.mark.django_db
def test_user_throttle_rate(client, settings, enable_throttle_rates, token_headers):
    rate = int(
        settings.REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"]["user"].removesuffix("/day")
    )
    url = reverse("user-me")
    for _ in range(rate):
        r = client.get(url, **token_headers)
        assert r.status_code == status.HTTP_200_OK
    r = client.get(url, **token_headers)
    assert r.status_code == status.HTTP_429_TOO_MANY_REQUESTS
