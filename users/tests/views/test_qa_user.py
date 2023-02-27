from django.urls import reverse

import pytest
from rest_framework import status

from notifier.models import Event
from users.models import User
from users.tests.factories import TEST_PASSWORD, UserFactory


@pytest.fixture(autouse=True)
def _qa_creds(settings):
    settings.CYPRESS_AUTH_SECRET = "secret"
    settings.CYPRESS_QA_USER_EMAIL1 = "qa1@email.com"
    settings.CYPRESS_QA_USER_EMAIL2 = "qa2@email.com"
    settings.CYPRESS_QA_USER_PASSWORD = TEST_PASSWORD


@pytest.mark.django_db()
def test_seed_qa_user_with_relatively_dated_events(client, settings):
    assert not User.objects.exists()
    url = reverse("seed-qa-user")
    r = client.post(url, data={"dataset": "relative"})
    assert r.status_code == status.HTTP_401_UNAUTHORIZED
    r = client.post(
        url, data={"auth": settings.CYPRESS_AUTH_SECRET, "dataset": "relative"}
    )
    assert r.status_code == status.HTTP_201_CREATED
    assert r.data["email"] == settings.CYPRESS_QA_USER_EMAIL1
    assert len(r.data["events_today"]) == 2
    assert len(r.data["events_upcoming"]) == 2
    assert len(r.data["all_events"]) == 10
    assert User.objects.count() == 1
    u = User.objects.get()
    assert u.check_password(settings.CYPRESS_QA_USER_PASSWORD)


@pytest.mark.django_db()
def test_seed_qa_user_with_statically_dated_events(client, settings):
    assert not User.objects.exists()
    url = reverse("seed-qa-user")
    r = client.post(url)
    assert r.status_code == status.HTTP_401_UNAUTHORIZED
    r = client.post(url, data={"auth": settings.CYPRESS_AUTH_SECRET})
    assert r.status_code == status.HTTP_201_CREATED
    assert r.data["email"] == settings.CYPRESS_QA_USER_EMAIL1
    assert len(r.data["all_events"]) == 4
    assert User.objects.count() == 1
    u = User.objects.get()
    assert u.check_password(settings.CYPRESS_QA_USER_PASSWORD)


@pytest.mark.django_db()
def test_seed_qa_user_replaces_existing_qa_user_with_email1(client, settings):
    u1 = UserFactory(
        email=settings.CYPRESS_QA_USER_EMAIL1,
        password=settings.CYPRESS_QA_USER_PASSWORD,
    )
    url = reverse("seed-qa-user")
    r = client.post(url, data={"auth": settings.CYPRESS_AUTH_SECRET})
    assert r.status_code == status.HTTP_201_CREATED
    assert r.data["email"] == settings.CYPRESS_QA_USER_EMAIL1
    assert User.objects.count() == 1
    u2 = User.objects.get()
    assert u2.check_password(settings.CYPRESS_QA_USER_PASSWORD)
    assert not User.objects.filter(pk=u1.pk).exists()


@pytest.mark.django_db()
def test_delete_qa_users(client, settings):
    UserFactory(
        email=settings.CYPRESS_QA_USER_EMAIL1,
        password=settings.CYPRESS_QA_USER_PASSWORD,
    )
    UserFactory(
        email=settings.CYPRESS_QA_USER_EMAIL2,
        password=settings.CYPRESS_QA_USER_PASSWORD,
    )
    assert User.objects.count() == 2
    url = reverse("seed-qa-user")
    r = client.delete(url)
    assert r.status_code == status.HTTP_401_UNAUTHORIZED
    r = client.delete(
        url,
        data={"auth": settings.CYPRESS_AUTH_SECRET},
        content_type="application/json",
    )
    assert r.status_code == status.HTTP_204_NO_CONTENT
    assert not User.objects.exists()
    assert not Event.objects.exists()
