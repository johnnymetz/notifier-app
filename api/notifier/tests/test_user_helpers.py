import datetime

import pytest

from notifier.constants import UNKNOWN_YEAR
from notifier.tests.factories import FriendFactory, UserFactory
from notifier.user_helpers import (
    get_friends_with_birthday_today,
    get_friends_with_birthday_within,
)


@pytest.mark.freeze_time("2020-01-01")
@pytest.mark.django_db
def test_get_friends_with_birthday_today(settings):
    settings.TIME_ZONE = "UTC"
    user = UserFactory()
    user2 = UserFactory()
    friend1 = FriendFactory(user=user, date_of_birth=datetime.datetime(1990, 1, 1))
    friend2 = FriendFactory(
        user=user, date_of_birth=datetime.datetime(UNKNOWN_YEAR, 1, 1)
    )
    FriendFactory(user=user, date_of_birth=datetime.datetime(1990, 1, 2))
    FriendFactory(user=user, date_of_birth=datetime.datetime(UNKNOWN_YEAR, 1, 3))
    FriendFactory(user=user2, date_of_birth=datetime.datetime(1990, 1, 1))
    friends = get_friends_with_birthday_today(user)
    assert friend1 in friends
    assert friend2 in friends
    assert friends.count() == 2


@pytest.mark.freeze_time("2020-01-01")
@pytest.mark.django_db
def test_get_friends_with_birthday_within(settings):
    settings.TIME_ZONE = "UTC"
    user = UserFactory()
    user2 = UserFactory()
    friend1 = FriendFactory(user=user, date_of_birth=datetime.datetime(1990, 1, 2))
    friend2 = FriendFactory(user=user, date_of_birth=datetime.datetime(1990, 1, 5))
    friend3 = FriendFactory(
        user=user, date_of_birth=datetime.datetime(UNKNOWN_YEAR, 1, 2)
    )
    friend4 = FriendFactory(
        user=user, date_of_birth=datetime.datetime(UNKNOWN_YEAR, 1, 5)
    )
    FriendFactory(user=user, date_of_birth=datetime.datetime(1990, 1, 1))
    FriendFactory(user=user, date_of_birth=datetime.datetime(1990, 1, 6))
    FriendFactory(user=user, date_of_birth=datetime.datetime(1989, 12, 31))
    FriendFactory(user=user, date_of_birth=datetime.datetime(UNKNOWN_YEAR, 1, 1))
    FriendFactory(user=user, date_of_birth=datetime.datetime(UNKNOWN_YEAR, 1, 6))
    FriendFactory(user=user, date_of_birth=datetime.datetime(UNKNOWN_YEAR, 12, 31))
    FriendFactory(user=user2, date_of_birth=datetime.datetime(1990, 1, 2))
    friends = get_friends_with_birthday_within(user, days=5)
    assert friend1 in friends
    assert friend2 in friends
    assert friend3 in friends
    assert friend4 in friends
    assert len(friends) == 4
    assert [f.birthday_display for f in friends] == ["01-02", "01-02", "01-05", "01-05"]


@pytest.mark.freeze_time("2020-01-30")
@pytest.mark.django_db
def test_get_friends_with_birthday_within_end_of_month(settings):
    settings.TIME_ZONE = "UTC"
    user = UserFactory()
    friend1 = FriendFactory(user=user, date_of_birth=datetime.datetime(1990, 1, 31))
    friend2 = FriendFactory(user=user, date_of_birth=datetime.datetime(1990, 2, 1))
    friend3 = FriendFactory(
        user=user, date_of_birth=datetime.datetime(UNKNOWN_YEAR, 1, 31)
    )
    friend4 = FriendFactory(
        user=user, date_of_birth=datetime.datetime(UNKNOWN_YEAR, 2, 2)
    )
    FriendFactory(user=user, date_of_birth=datetime.datetime(1990, 1, 30))
    FriendFactory(user=user, date_of_birth=datetime.datetime(1990, 2, 10))
    FriendFactory(user=user, date_of_birth=datetime.datetime(UNKNOWN_YEAR, 1, 30))
    FriendFactory(user=user, date_of_birth=datetime.datetime(UNKNOWN_YEAR, 2, 10))
    friends = get_friends_with_birthday_within(user, days=5)
    assert friend1 in friends
    assert friend2 in friends
    assert friend3 in friends
    assert friend4 in friends
    assert len(friends) == 4
