import pytest

from notifier.tests.factories import FriendFactory
from users.serializers import UserSerializer
from users.tests.factories import UserFactory


@pytest.mark.django_db
def test_read_user_fields():
    u = UserFactory()
    friend1 = FriendFactory(user=u)
    friend2 = FriendFactory(user=u)
    friend3 = FriendFactory(user=u)
    data = UserSerializer(u).data
    assert data["id"] == u.id
    assert data["email"] == u.email
    assert "password" not in data
    assert len(data["all_friends"]) == 3
    assert sorted([f["id"] for f in data["all_friends"]]) == sorted(
        [friend1.id, friend2.id, friend3.id]
    )
    assert "upcoming_friends" in data
