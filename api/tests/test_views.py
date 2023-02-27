from django.urls import reverse

from rest_framework import status


def test_welcome_view(client, settings):
    assert settings.DEBUG is True
    url = reverse("welcome")
    r = client.get(url)
    assert r.status_code == status.HTTP_200_OK
