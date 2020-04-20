import datetime

import pytest
import pytz
from django.core.exceptions import ValidationError
from django.utils import timezone
from freezegun import freeze_time
from notifier.models import Friend
from notifier.tests.factories import FriendFactory, UserFactory


@freeze_time("2020-01-01")
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


@pytest.mark.django_db
def test_create_friend():
    user = UserFactory()
    today = timezone.localdate()
    friend = Friend.objects.create(user=user, first_name="First", date_of_birth=today)
    assert friend in Friend.objects.all()


@pytest.mark.django_db
def test_friend_factory_is_valid():
    FriendFactory()


@pytest.mark.django_db
def test_friend_birthday_display():
    friend = FriendFactory(date_of_birth=datetime.datetime(2000, 2, 2))
    assert friend.birthday_display == "02/02"
    friend_no_year = FriendFactory(date_of_birth=None, month=3, day=3)
    assert friend_no_year.birthday_display == "03/03"


@freeze_time("2020-01-01")
@pytest.mark.django_db
def test_friend_age(settings):
    settings.TIME_ZONE = "UTC"
    assert FriendFactory(date_of_birth=datetime.datetime(2000, 1, 2)).age == 19
    assert FriendFactory(date_of_birth=datetime.datetime(2000, 2, 1)).age == 19
    assert FriendFactory(date_of_birth=datetime.datetime(2000, 1, 1)).age == 20
    assert FriendFactory(date_of_birth=datetime.datetime(1999, 11, 30)).age == 20
    assert FriendFactory(date_of_birth=datetime.datetime(1999, 12, 31)).age == 20


@pytest.mark.django_db
def test_only_month_or_day_without_dob_raises_error():
    msg = "Both month and day are required if date_of_birth is None"
    with pytest.raises(ValidationError) as e:
        FriendFactory(date_of_birth=None)
    assert e.value.message == msg
    with pytest.raises(ValidationError) as e:
        FriendFactory(date_of_birth=None, month=3)
    assert e.value.message == msg
    with pytest.raises(ValidationError) as e:
        FriendFactory(date_of_birth=None, day=3)
    assert e.value.message == msg


@pytest.mark.django_db
def test_adding_month_or_day_with_dob_raises_error():
    msg = "Neither month nor day can be set if date_of_birth is provided"
    with pytest.raises(ValidationError) as e:
        FriendFactory(month=3)
    assert e.value.message == msg
    with pytest.raises(ValidationError) as e:
        FriendFactory(day=3)
    assert e.value.message == msg
    with pytest.raises(ValidationError) as e:
        FriendFactory(month=3, day=3)
    assert e.value.message == msg
