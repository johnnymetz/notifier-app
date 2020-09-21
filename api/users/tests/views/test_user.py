from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse

import djoser.utils
import pytest
from rest_framework import status

from users.tests.factories import UserFactory

User = get_user_model()


@pytest.mark.django_db
def test_unauthenticated_read_user_detail(client):
    url = reverse("user-detail")
    r = client.get(url)
    assert r.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_read_user_detail(client, token_headers):
    u = User.objects.get()
    url = reverse("user-detail")
    r = client.get(url, **token_headers)
    assert r.status_code == status.HTTP_200_OK
    assert r.data["id"] == u.id


@pytest.mark.django_db
def test_create_user(client, mailoutbox, settings):
    url = reverse("user-list")
    data = {"email": "jj@email.com", "password": "pw123", "re_password": "pw123"}
    r = client.post(url, data=data)
    assert r.status_code == status.HTTP_201_CREATED
    assert r.data["email"] == "jj@email.com"
    assert len(mailoutbox) == 1
    assert settings.DOMAIN in mailoutbox[0].body
    assert settings.SITE_NAME in mailoutbox[0].body
    assert User.objects.count() == 1
    u = User.objects.get(pk=r.data["id"])
    assert not u.is_active
    assert not u.is_staff
    assert not u.is_superuser


@pytest.mark.django_db
def test_activate_user(client, mailoutbox):
    u = UserFactory(is_active=False)
    url = reverse("user-activation")
    data = {
        "uid": djoser.utils.encode_uid(u.pk),
        "token": default_token_generator.make_token(u),
    }
    r = client.get(url, data=data)
    assert r.status_code == status.HTTP_204_NO_CONTENT
    assert len(mailoutbox) == 1
    u.refresh_from_db()
    assert u.is_active


# test updating user (patch)
# test deactivating user (is_active=False)


@pytest.mark.django_db
def test_reset_password(client, mailoutbox):
    u = UserFactory()
    url = reverse("user-reset-password")
    data = {"email": u.email}
    r = client.post(url, data=data)
    assert r.status_code == status.HTTP_204_NO_CONTENT
    assert len(mailoutbox) == 1
