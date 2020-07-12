import pytest

from notifier.serializers import FriendSerializer, UserSerializer
from notifier.tests.factories import FriendFactory, UserFactory


@pytest.mark.django_db
def test_friend_fields():
    friend = FriendFactory()
    data = FriendSerializer(friend).data
    assert data["id"] == friend.id
    assert data["user"] == friend.user.id
    assert data["first_name"] == friend.first_name
    assert data["last_name"] == friend.last_name
    assert data["birthday"] == friend.birthday_display
    assert data["age"] == friend.age


@pytest.mark.django_db
def test_user_fields():
    u = UserFactory()
    friend1 = FriendFactory(user=u)
    friend2 = FriendFactory(user=u)
    friend3 = FriendFactory(user=u)
    data = UserSerializer(u).data
    assert data["id"] == u.id
    assert data["username"] == u.username
    assert "password" not in data
    assert data["email"] == u.email
    assert len(data["friends"]) == 3
    assert sorted([f["id"] for f in data["friends"]]) == sorted(
        [friend1.id, friend2.id, friend3.id]
    )
