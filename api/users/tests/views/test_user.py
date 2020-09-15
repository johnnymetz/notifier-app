from django.contrib.auth import get_user_model
from django.urls import reverse

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
def test_create_user(client):
    url = reverse("user-list")
    data = {"email": "jj@email.com", "password": "pw123", "re_password": "pw123"}
    r = client.post(url, data=data)
    assert r.status_code == status.HTTP_201_CREATED
    assert r.data["email"] == "jj@email.com"
    assert User.objects.count() == 1


# @pytest.mark.django_db
# def test_activate_user(client):
#     import djoser.utils
#     u = UserFactory()
#     print(u.pk)
#     print(djoser.utils.encode_uid(u.pk))
# url = reverse("user-activation")
# print(url)
# data = {"uid": "jj@email.com", "token": "pw123"}
# r = client.post(url, data=data)
# print(r.status_code)
# print(r.data)


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
