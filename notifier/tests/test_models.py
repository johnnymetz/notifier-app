import datetime

from django.core.exceptions import ValidationError
from django.utils import timezone

import pytest

from notifier.exceptions import NotifierError
from notifier.models import Event
from notifier.tests.factories import EventFactory
from users.tests.factories import UserFactory


@pytest.mark.django_db()
def test_create_event():
    user = UserFactory()
    today = timezone.localdate()
    event = Event.objects.create(
        user=user, name="JJ Reddick", annual_date=today, type=Event.EventType.BIRTHDAY
    )
    assert event in Event.objects.all()


@pytest.mark.django_db()
def test_event_annual_date_display():
    event = EventFactory(annual_date=datetime.date(2000, 2, 2))
    assert event.annual_date_display == "02-02"


@pytest.mark.freeze_time("2020-01-01")
@pytest.mark.django_db()
def test_event_age(settings):
    settings.TIME_ZONE = "UTC"
    assert EventFactory(annual_date=datetime.date(2000, 1, 2)).age == 19
    assert EventFactory(annual_date=datetime.date(2000, 2, 1)).age == 19
    assert EventFactory(annual_date=datetime.date(2000, 1, 1)).age == 20
    assert EventFactory(annual_date=datetime.date(1999, 11, 30)).age == 20
    assert EventFactory(annual_date=datetime.date(1999, 12, 31)).age == 20
    assert EventFactory(annual_date=datetime.date(2020, 1, 1)).age == 0
    assert EventFactory(annual_date=datetime.date(2020, 1, 2)).age == -1
    assert EventFactory(annual_date=datetime.date(2020, 2, 2)).age == -1
    assert EventFactory(annual_date=datetime.date(2021, 1, 2)).age == -2


@pytest.mark.django_db()
def test_event_name_validation():
    event = EventFactory()
    with pytest.raises(ValidationError):
        EventFactory(name=event.name)


@pytest.mark.django_db()
def test_user_events_limit_validation(settings):
    user = UserFactory()
    for _ in range(settings.MAX_EVENTS_PER_USER):
        EventFactory(user=user)
    assert user.events.count() == settings.MAX_EVENTS_PER_USER
    msg = f"{user} has reached the event limit"
    with pytest.raises(NotifierError, match=msg):
        EventFactory(user=user)
