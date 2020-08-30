from django.urls import reverse

import pytest

from notifier.tests.factories import UserFactory


@pytest.fixture
def token_headers(client):
    url = reverse("jwt-create")
    pw = "pass"
    u = UserFactory(password=pw)
    r = client.post(url, {"email": u.email, "password": pw})
    access_token = r.data["access"]
    headers = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}
    return headers
