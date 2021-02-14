from django.core.cache import cache
from django.urls import reverse

import pytest
from nplusone.core.profiler import Profiler

from users.tests.factories import TEST_PASSWORD, UserFactory


@pytest.fixture(autouse=True)
def _ensure_test_settings(settings):
    assert settings.SETTINGS_MODULE == "api.settings.test", "Must use the test settings"


@pytest.fixture(autouse=True)
def _clear_cache():
    cache.clear()  # clear throttling limit cache


@pytest.fixture(autouse=True)
def _raise_nplusone(request):
    if request.node.get_closest_marker("skip_nplusone"):
        yield
    else:
        with Profiler():
            yield


@pytest.fixture()
def token_headers(client):
    url = reverse("jwt-create")
    u = UserFactory(password=TEST_PASSWORD)
    r = client.post(url, {"email": u.email, "password": TEST_PASSWORD})
    access_token = r.data["access"]
    return {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}
