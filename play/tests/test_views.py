from unittest.mock import patch

from django.conf import settings

import pytest
from rest_framework import status

from notifier.exceptions import NotifierError
from play.views import DEFAULT_TIMEOUT


class TestThrowView:
    @pytest.fixture(autouse=True)
    def _configure(self, settings):
        settings.CYPRESS_AUTH_SECRET = "secret"

    def test_no_auth_raises_401(self, client):
        response = client.post("/api/play/throw/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_throw(self, client):
        with pytest.raises(NotifierError):
            client.post("/api/play/throw/", {"auth": settings.CYPRESS_AUTH_SECRET})


class TestTimeoutView:
    @pytest.fixture(autouse=True)
    def _configure(self, settings):
        settings.CYPRESS_AUTH_SECRET = "secret"

    def test_no_auth_raises_401(self, client):
        response = client.post("/api/play/timeout/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_invalid_seconds_input_raises_400(self, client):
        response = client.post(
            "/api/play/timeout/",
            {"auth": settings.CYPRESS_AUTH_SECRET, "seconds": "xxx"},
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == ["Invalid seconds input: xxx"]

    @patch("time.sleep")
    def test_timeout_default(self, mock_sleep, client):
        response = client.post(
            "/api/play/timeout/", {"auth": settings.CYPRESS_AUTH_SECRET}
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        # mock_sleep.assert_called_once_with(DEFAULT_TIMEOUT)
        assert mock_sleep.call_count == DEFAULT_TIMEOUT

    @patch("time.sleep")
    def test_timeout(self, mock_sleep, client):
        sec = 5
        assert sec != DEFAULT_TIMEOUT
        response = client.post(
            "/api/play/timeout/", {"auth": settings.CYPRESS_AUTH_SECRET, "seconds": sec}
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        # mock_sleep.assert_called_once_with(sec)
        assert mock_sleep.call_count == sec
