from django.contrib.auth import get_user_model
from django.urls import reverse

import pytest
from rest_framework import status


@pytest.mark.django_db
def test_unauthenticated_read_user_detail(client):
    url = reverse("user-detail")
    r = client.get(url)
    assert r.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_read_user_detail(client, token_headers):
    User = get_user_model()
    u = User.objects.get()
    url = reverse("user-detail")
    r = client.get(url, **token_headers)
    assert r.status_code == status.HTTP_200_OK
    assert r.data["id"] == u.id


@pytest.mark.django_db
def test_seed_qa_user(monkeypatch, client):
    monkeypatch.setenv("QA_USER_EMAIL", "qa@email.com")
    url = reverse("seed-qa-user")
    r = client.post(url)
    assert r.status_code == status.HTTP_401_UNAUTHORIZED
    r = client.post(url, {"auth": "Cypress789"})
    assert r.status_code == status.HTTP_201_CREATED
    assert r.data["email"] == "qa@email.com"
    assert len(r.data["all_friends"]) == 4


# test creating new user (post)
# test updating user (patch)
# test deactivating user (is_active=False)
