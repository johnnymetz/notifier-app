from types import SimpleNamespace

from django.contrib.auth import get_user_model
from django.urls import reverse

import pytest
from rest_framework import status

from notifier.models import Event
from users.tests.factories import TEST_PASSWORD, UserFactory

User = get_user_model()


@pytest.fixture
def qa_creds(monkeypatch):
    email1 = "qa1@email.com"
    email2 = "qa2@email.com"
    pw = TEST_PASSWORD
    monkeypatch.setenv("QA_USER_EMAIL1", email1)
    monkeypatch.setenv("QA_USER_EMAIL2", email2)
    monkeypatch.setenv("QA_USER_PASSWORD", pw)
    return SimpleNamespace(email1=email1, email2=email2, password=pw)


@pytest.mark.django_db
def test_seed_qa_user(qa_creds, client):
    assert not User.objects.exists()
    url = reverse("seed-qa-user")
    r = client.post(url)
    assert r.status_code == status.HTTP_401_UNAUTHORIZED
    r = client.post(url, data={"auth": "Cypress789"})
    assert r.status_code == status.HTTP_201_CREATED
    assert r.data["email"] == qa_creds.email1
    assert len(r.data["all_events"]) == 4
    assert User.objects.count() == 1
    u = User.objects.get()
    assert u.check_password(qa_creds.password)


@pytest.mark.django_db
def test_seed_qa_user_replaces_existing_qa_user_with_email1(qa_creds, client):
    u1 = UserFactory(email=qa_creds.email1, password=qa_creds.password)
    url = reverse("seed-qa-user")
    r = client.post(url, data={"auth": "Cypress789"})
    assert r.status_code == status.HTTP_201_CREATED
    assert r.data["email"] == qa_creds.email1
    assert User.objects.count() == 1
    u2 = User.objects.get()
    assert u2.check_password(qa_creds.password)
    assert not User.objects.filter(pk=u1.pk).exists()


@pytest.mark.django_db
def test_delete_qa_users(qa_creds, client):
    UserFactory(email=qa_creds.email1, password=qa_creds.password)
    UserFactory(email=qa_creds.email2, password=qa_creds.password)
    assert User.objects.count() == 2
    url = reverse("seed-qa-user")
    r = client.delete(url)
    assert r.status_code == status.HTTP_401_UNAUTHORIZED
    r = client.delete(url, data={"auth": "Cypress789"}, content_type="application/json")
    assert r.status_code == status.HTTP_204_NO_CONTENT
    assert not User.objects.exists()
    assert not Event.objects.exists()
