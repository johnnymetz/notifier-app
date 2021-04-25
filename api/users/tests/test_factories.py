import pytest

from users.tests.factories import UserFactory


@pytest.mark.django_db()
def test_user_factory():
    u = UserFactory()
    assert u.username is None
    assert u.email
    assert len(u.password) > 20, "Password should be a hash"
    assert u.is_active
    assert not u.is_staff
    assert not u.is_superuser


@pytest.mark.django_db()
def test_superuser_factory():
    u = UserFactory(is_superuser=True)
    assert u.username is None
    assert u.email
    assert len(u.password) > 20, "Password should be a hash"
    assert u.is_active
    assert not u.is_staff
    assert u.is_superuser
