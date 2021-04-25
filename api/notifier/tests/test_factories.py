import pytest

from notifier.tests.factories import EventFactory


@pytest.mark.django_db()
def test_event_factory():
    EventFactory()
