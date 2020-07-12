import datetime

from django.utils import timezone

import pytest
import pytz

from notifier.tests.factories import FriendFactory, UserFactory


@pytest.mark.django_db
def test_user_factory():
    u = UserFactory()
    assert u.email == f"{u.username}@email.com"
    assert len(u.password) > 20, "Password should be a hash"
    assert u.is_active
    assert not u.is_staff
    assert not u.is_superuser


@pytest.mark.django_db
def test_superuser_factory():
    u = UserFactory(is_superuser=True)
    assert u.email == f"{u.username}@email.com"
    assert len(u.password) > 20, "Password should be a hash"
    assert u.is_active
    assert not u.is_staff
    assert u.is_superuser


@pytest.mark.django_db
def test_friend_factory():
    FriendFactory()


@pytest.mark.freeze_time("2020-01-01")
def test_freeze_time_functionality():
    # print(timezone.now())  # UTC time
    # print(timezone.localdate())  # Local date
    # print(timezone.localtime())  # Local datetime
    assert datetime.datetime.now(tz=pytz.timezone("UTC")) == timezone.now()
    assert (
        datetime.datetime.now(tz=pytz.timezone("America/Los_Angeles"))
        == timezone.localtime()
    )
    assert datetime.datetime.now().date() == timezone.localdate(
        timezone=pytz.timezone("UTC")
    )
    assert datetime.datetime.now() == datetime.datetime.today()
