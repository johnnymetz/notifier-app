from django.core.cache import cache
from django.urls import reverse

import pytest

from users.tests.factories import TEST_PASSWORD, UserFactory


@pytest.fixture(autouse=True)
def setup():
    cache.clear()  # clear throttling limit cache


@pytest.fixture
def token_headers(client):
    url = reverse("jwt-create")
    u = UserFactory(password=TEST_PASSWORD)
    r = client.post(url, {"email": u.email, "password": TEST_PASSWORD})
    access_token = r.data["access"]
    headers = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}
    return headers
