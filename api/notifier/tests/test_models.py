import datetime

from django.utils import timezone

import pytest

from notifier.models import Friend
from notifier.tests.factories import FriendFactory, UserFactory


@pytest.mark.django_db
def test_create_friend():
    user = UserFactory()
    today = timezone.localdate()
    friend = Friend.objects.create(user=user, first_name="First", date_of_birth=today)
    assert friend in Friend.objects.all()


@pytest.mark.django_db
def test_friend_birthday_display():
    friend = FriendFactory(date_of_birth=datetime.datetime(2000, 2, 2))
    assert friend.birthday_display == "02-02"


@pytest.mark.freeze_time("2020-01-01")
@pytest.mark.django_db
def test_friend_age(settings):
    settings.TIME_ZONE = "UTC"
    assert FriendFactory(date_of_birth=datetime.datetime(2000, 1, 2)).age == 19
    assert FriendFactory(date_of_birth=datetime.datetime(2000, 2, 1)).age == 19
    assert FriendFactory(date_of_birth=datetime.datetime(2000, 1, 1)).age == 20
    assert FriendFactory(date_of_birth=datetime.datetime(1999, 11, 30)).age == 20
    assert FriendFactory(date_of_birth=datetime.datetime(1999, 12, 31)).age == 20
