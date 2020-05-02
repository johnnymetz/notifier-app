import datetime

import pytest
from freezegun import freeze_time
from notifier.helpers import (
    get_birthday_display,
    get_friends_with_birthday_today,
    get_friends_with_birthday_within,
)
from notifier.tests.factories import FriendFactory, UserFactory


def test_get_birthday_display():
    assert get_birthday_display(datetime.date(2000, 2, 2)) == "02/02"
    assert get_birthday_display(None, month=3, day=3) == "03/03"


@freeze_time("2020-01-01")
@pytest.mark.django_db
def test_get_friends_with_birthday_today(settings):
    settings.TIME_ZONE = "UTC"
    user = UserFactory()
    user2 = UserFactory()
    friend1 = FriendFactory(user=user, date_of_birth=datetime.datetime(1990, 1, 1))
    friend2 = FriendFactory(user=user, date_of_birth=None, month=1, day=1)
    FriendFactory(user=user, date_of_birth=datetime.datetime(1990, 1, 2))
    FriendFactory(user=user, date_of_birth=None, month=1, day=3)
    FriendFactory(user=user2, date_of_birth=datetime.datetime(1990, 1, 1))
    friends = get_friends_with_birthday_today(user)
    assert friend1 in friends
    assert friend2 in friends
    assert friends.count() == 2


@freeze_time("2020-01-01")
@pytest.mark.django_db
def test_get_friends_with_birthday_within(settings):
    settings.TIME_ZONE = "UTC"
    user = UserFactory()
    user2 = UserFactory()
    friend1 = FriendFactory(user=user, date_of_birth=datetime.datetime(1990, 1, 2))
    friend2 = FriendFactory(user=user, date_of_birth=datetime.datetime(1990, 1, 5))
    friend3 = FriendFactory(user=user, date_of_birth=None, month=1, day=2)
    friend4 = FriendFactory(user=user, date_of_birth=None, month=1, day=5)
    FriendFactory(user=user, date_of_birth=datetime.datetime(1990, 1, 1))
    FriendFactory(user=user, date_of_birth=datetime.datetime(1990, 1, 6))
    FriendFactory(user=user, date_of_birth=datetime.datetime(1989, 12, 31))
    FriendFactory(user=user, date_of_birth=None, month=1, day=1)
    FriendFactory(user=user, date_of_birth=None, month=1, day=6)
    FriendFactory(user=user, date_of_birth=None, month=12, day=31)
    FriendFactory(user=user2, date_of_birth=datetime.datetime(1990, 1, 2))
    friends = get_friends_with_birthday_within(user, days=5)
    assert friend1 in friends
    assert friend2 in friends
    assert friend3 in friends
    assert friend4 in friends
    assert len(friends) == 4
    assert [f.birthday_display for f in friends] == ["01/02", "01/02", "01/05", "01/05"]
