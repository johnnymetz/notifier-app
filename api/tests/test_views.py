from django.urls import reverse

from rest_framework import status


def test_welcome_view(client, settings):
    assert settings.SECURE_SSL_HOST is None
    assert settings.SECURE_PROXY_SSL_HEADER is None
    assert settings.SECURE_SSL_REDIRECT is False
    url = reverse("welcome")
    r = client.get(url)
    assert r.status_code == status.HTTP_200_OK
