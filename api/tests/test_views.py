from django.urls import reverse

from rest_framework import status


def test_welcome_view(client):
    url = reverse("welcome")
    r = client.get("/")
    assert r.status_code == status.HTTP_200_OK, url
