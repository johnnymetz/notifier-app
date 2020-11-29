import pytest

from notifier.tests.factories import EventFactory
from users.serializers import UserSerializer
from users.tests.factories import UserFactory


@pytest.mark.django_db
def test_read_user_fields():
    u = UserFactory()
    event1 = EventFactory(user=u)
    event2 = EventFactory(user=u)
    event3 = EventFactory(user=u)
    data = UserSerializer(u).data
    assert data["id"] == u.id
    assert data["email"] == u.email
    assert data["is_subscribed"] == u.is_subscribed
    assert "password" not in data
    assert len(data["all_events"]) == 3
    assert sorted([f["id"] for f in data["all_events"]]) == sorted(
        [event1.id, event2.id, event3.id]
    )
    assert "events_today" in data
    assert "events_upcoming" in data
