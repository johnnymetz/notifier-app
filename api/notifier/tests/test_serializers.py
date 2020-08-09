import datetime

import pytest

from notifier.constants import UNKNOWN_YEAR
from notifier.serializers import FriendSerializer, UserSerializer
from notifier.tests.factories import FriendFactory, UserFactory


@pytest.mark.django_db
def test_read_friend_fields():
    friend = FriendFactory()
    data = FriendSerializer(friend).data
    assert data["id"] == friend.id
    assert data["user"] == friend.user.id
    assert data["name"] == friend.name
    assert data["date_of_birth"]["year"] == friend.date_of_birth.year
    assert data["date_of_birth"]["month"] == friend.date_of_birth.month
    assert data["date_of_birth"]["day"] == friend.date_of_birth.day
    assert data["age"] == friend.age


@pytest.mark.django_db
def test_read_friend_fields_without_bday_year():
    friend = FriendFactory()
    friend.date_of_birth = friend.date_of_birth.replace(year=UNKNOWN_YEAR)
    data = FriendSerializer(friend).data
    assert data["id"] == friend.id
    assert data["user"] == friend.user.id
    assert data["name"] == friend.name
    assert data["date_of_birth"]["year"] is None
    assert data["date_of_birth"]["month"] == friend.date_of_birth.month
    assert data["date_of_birth"]["day"] == friend.date_of_birth.day
    assert data["age"] == friend.age


@pytest.mark.django_db
def test_create_friend(rf):
    u = UserFactory()
    date = datetime.date(1994, 1, 24)
    data = {
        "name": "JJ Reddick",
        "date_of_birth": {"year": date.year, "month": date.month, "day": date.day},
    }
    request = rf.post("/whatever")
    request.user = u
    serializer = FriendSerializer(data=data, context={"request": request})
    assert serializer.is_valid(raise_exception=True)
    friend = serializer.save()
    assert friend.name == data["name"]
    assert friend.date_of_birth == date
    assert friend.user == u


@pytest.mark.django_db
def test_update_friend():
    u = UserFactory()
    friend = FriendFactory(user=u)
    date = datetime.date(1994, 1, 24)
    data = {
        "name": "JJ Reddick",
        "date_of_birth": {"year": date.year, "month": date.month, "day": date.day},
    }
    serializer = FriendSerializer(friend, data=data)
    assert serializer.is_valid(raise_exception=True)
    friend = serializer.save()
    assert friend.name == data["name"]
    assert friend.date_of_birth == date
    assert friend.user == u


@pytest.mark.django_db
def test_update_friend_without_bday_year():
    u = UserFactory()
    friend = FriendFactory(user=u)
    date = datetime.date(1994, 1, 24)
    data = {
        "name": "JJ Reddick",
        "date_of_birth": {"month": date.month, "day": date.day},
    }
    serializer = FriendSerializer(friend, data=data)
    assert serializer.is_valid(raise_exception=True)
    friend = serializer.save()
    assert friend.name == data["name"]
    assert friend.date_of_birth == datetime.date(UNKNOWN_YEAR, date.month, date.day)
    assert friend.user == u


@pytest.mark.django_db
def test_read_user_fields():
    u = UserFactory()
    friend1 = FriendFactory(user=u)
    friend2 = FriendFactory(user=u)
    friend3 = FriendFactory(user=u)
    data = UserSerializer(u).data
    assert data["id"] == u.id
    assert data["username"] == u.username
    assert "password" not in data
    assert data["email"] == u.email
    assert len(data["all_friends"]) == 3
    assert sorted([f["id"] for f in data["all_friends"]]) == sorted(
        [friend1.id, friend2.id, friend3.id]
    )
    assert "upcoming_friends" in data
