from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse

import djoser.utils
import pytest
from rest_framework import status

from notifier.tests.factories import EventFactory
from users.tests.factories import TEST_PASSWORD, UserFactory

User = get_user_model()


@pytest.mark.django_db()
def test_read_current_user(client, token_headers):
    u = User.objects.get()
    EventFactory(user=u)
    UserFactory()
    url = reverse("user-me")
    r = client.get(url)
    assert r.status_code == status.HTTP_401_UNAUTHORIZED
    r = client.get(url, **token_headers)
    assert r.status_code == status.HTTP_200_OK
    assert r.data["id"] == u.id
    assert len(r.data["all_events"]) == 1
    assert "events_today" in r.data
    assert "events_upcoming" in r.data


@pytest.mark.django_db()
def test_create_user(client, mailoutbox, settings):
    url = reverse("user-list")
    data = {
        "email": "jj@email.com",
        "password": TEST_PASSWORD,
        "re_password": TEST_PASSWORD,
    }
    r = client.post(url, data=data)
    assert r.status_code == status.HTTP_201_CREATED
    assert r.data["email"] == "jj@email.com"
    assert len(mailoutbox) == 1
    assert settings.DOMAIN in mailoutbox[0].body
    assert settings.SITE_NAME in mailoutbox[0].body
    assert User.objects.count() == 1
    u = User.objects.get(pk=r.data["id"])
    assert u.check_password(TEST_PASSWORD)
    assert not u.is_active
    assert not u.is_staff
    assert not u.is_superuser


@pytest.mark.django_db()
def test_resend_activation_email(client, mailoutbox):
    u = UserFactory(is_active=False)
    url = reverse("user-resend-activation")
    r = client.post(url, data={"email": u.email})
    assert r.status_code == status.HTTP_204_NO_CONTENT
    assert len(mailoutbox) == 1


@pytest.mark.django_db()
def test_activate_user(client, mailoutbox):
    u = UserFactory(is_active=False)
    url = reverse("user-activation")
    data = {
        "uid": djoser.utils.encode_uid(u.pk),
        "token": default_token_generator.make_token(u),
    }
    r = client.post(url, data=data)
    assert r.status_code == status.HTTP_204_NO_CONTENT
    assert len(mailoutbox) == 1
    u.refresh_from_db()
    assert u.is_active


@pytest.mark.django_db()
def test_set_email(client, mailoutbox, token_headers):
    u = User.objects.get()
    url = reverse("user-set-username")
    new_email = "different@email.com"
    data = {
        "new_email": new_email,
        "re_new_email": new_email,
        "current_password": TEST_PASSWORD,
    }
    r = client.post(url, data=data, **token_headers)
    assert r.status_code == status.HTTP_204_NO_CONTENT
    assert len(mailoutbox) == 1
    u.refresh_from_db()
    assert u.email == new_email


@pytest.mark.django_db()
def test_set_password(client, mailoutbox, token_headers):
    u = User.objects.get()
    url = reverse("user-set-password")
    new_pw = "new_pw"
    assert new_pw != TEST_PASSWORD
    data = {
        "new_password": new_pw,
        "re_new_password": new_pw,
        "current_password": TEST_PASSWORD,
    }
    r = client.post(url, data=data, **token_headers)
    assert r.status_code == status.HTTP_204_NO_CONTENT
    assert len(mailoutbox) == 1
    u.refresh_from_db()
    assert u.check_password(new_pw)


@pytest.mark.django_db()
def test_update(client, mailoutbox, token_headers):
    u = User.objects.get()
    assert u.is_subscribed is True
    url = reverse("user-me")
    data = {"is_subscribed": False}
    r = client.patch(url, data=data, content_type="application/json", **token_headers)
    assert r.status_code == status.HTTP_200_OK
    assert r.data["is_subscribed"] is False
    # TODO: this sends an ActivationEmail, which should be removed from djoser master
    assert len(mailoutbox) == 1


@pytest.mark.django_db()
def test_send_reset_password_email(client, mailoutbox):
    u = UserFactory()
    url = reverse("user-reset-password")
    # email not found
    r = client.post(url, data={"email": "bad"})
    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert len(mailoutbox) == 0
    # email found
    r = client.post(url, data={"email": u.email})
    assert r.status_code == status.HTTP_204_NO_CONTENT
    assert len(mailoutbox) == 1


@pytest.mark.django_db()
def test_reset_password(client, mailoutbox):
    u = UserFactory()
    url = reverse("user-reset-password-confirm")
    new_pw = "new_pw"
    assert new_pw != TEST_PASSWORD
    data = {
        "uid": djoser.utils.encode_uid(u.pk),
        "token": default_token_generator.make_token(u),
        "new_password": new_pw,
        "re_new_password": new_pw,
    }
    r = client.post(url, data=data)
    assert r.status_code == status.HTTP_204_NO_CONTENT
    assert len(mailoutbox) == 1
    u.refresh_from_db()
    assert u.check_password(new_pw)
