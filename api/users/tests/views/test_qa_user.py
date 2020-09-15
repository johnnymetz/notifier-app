from django.contrib.auth import get_user_model
from django.urls import reverse

import pytest
from rest_framework import status


@pytest.mark.django_db
def test_seed_qa_user(monkeypatch, client):
    User = get_user_model()
    monkeypatch.setenv("QA_USER_EMAIL", "qa@email.com")
    monkeypatch.setenv("QA_USER_PASSWORD", "pw")
    url = reverse("seed-qa-user")
    r = client.post(url)
    assert r.status_code == status.HTTP_401_UNAUTHORIZED
    r = client.post(url, {"auth": "Cypress789"})
    assert r.status_code == status.HTTP_201_CREATED
    assert r.data["email"] == "qa@email.com"
    assert len(r.data["all_friends"]) == 4
    assert User.objects.count() == 1
