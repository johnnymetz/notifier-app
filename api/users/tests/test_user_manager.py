from django.contrib.auth import get_user_model

import pytest

User = get_user_model()


@pytest.mark.django_db
def test_create_user():
    user = User.objects.create_user(email="normal@user.com", password="foo")
    assert user.email == "normal@user.com"
    assert user.is_active
    assert not user.is_staff
    assert not user.is_superuser
    assert not user.username
    with pytest.raises(TypeError):
        User.objects.create_user()
    with pytest.raises(TypeError):
        User.objects.create_user(email="")
    with pytest.raises(ValueError, match="The Email must be set"):
        User.objects.create_user(email="", password="foo")
    assert user.is_subscribed


@pytest.mark.django_db
def test_create_superuser():
    admin_user = User.objects.create_superuser(email="super@user.com", password="foo")
    assert admin_user.email == "super@user.com"
    assert admin_user.is_active
    assert admin_user.is_staff
    assert admin_user.is_superuser
    assert not admin_user.username
    with pytest.raises(ValueError, match="Superuser must have is_superuser=True"):
        User.objects.create_superuser(
            email="super@user.com", password="foo", is_superuser=False
        )
    assert admin_user.is_subscribed
