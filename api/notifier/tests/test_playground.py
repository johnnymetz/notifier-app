"""
Some random tests for learning purposes.
"""
import datetime
import logging
from unittest.mock import Mock, create_autospec
from zoneinfo import ZoneInfo

from django.contrib.auth import get_user_model
from django.db import connection, reset_queries
from django.utils import timezone

import pytest
from nplusone.core.exceptions import NPlusOneError

from notifier.models import Event
from notifier.tests.factories import EventFactory, UserFactory

User = get_user_model()


@pytest.mark.freeze_time("2020-01-01")
def test_freeze_time_functionality():
    # print(timezone.now())  # UTC time
    # print(timezone.localdate())  # Local date
    # print(timezone.localtime())  # Local datetime
    assert datetime.datetime.now(tz=ZoneInfo("UTC")) == timezone.now()
    assert (
        datetime.datetime.now(tz=ZoneInfo("America/Los_Angeles"))
        == timezone.localtime()
    )
    assert datetime.datetime.now().date() == timezone.localdate(
        timezone=ZoneInfo("UTC")
    )
    assert datetime.datetime.now() == datetime.datetime.today()


@pytest.mark.django_db()
def test_nplusone(settings):
    settings.DEBUG = True  # debug must be True to populate connection.queries
    u1 = UserFactory()
    for _ in range(100):
        EventFactory(user=u1)

    reset_queries()
    for e in Event.objects.all():
        with pytest.raises(NPlusOneError):
            assert e.user

    reset_queries()
    for e in Event.objects.select_related("user"):
        assert e.user

    # sqlite will occasionally run an extra "EXPLAIN" query so let's exclude that
    queries = [
        x for x in connection.queries if not x["sql"].startswith("EXPLAIN QUERY PLAN")
    ]
    assert len(queries) == 1


def test_pytest_caplog(caplog):
    """https://stribny.name/blog/pytest/#logging"""
    logger = logging.getLogger("django")
    logger.info("One")
    logger.info("Two")
    assert "One" in caplog.text
    assert "Two" in caplog.text
    assert "Something else" not in caplog.text


# SPECCING: creating a mock object that has the same api/structure as the selected object
# https://blog.thea.codes/my-python-testing-style-guide/


def test_manually_define_mock():
    user = Mock()
    assert user.username
    assert user.nonexistent


def test_manually_spec_mock():
    user = Mock(spec=["username"], username="batman", x1=1)
    assert user.username == "batman"
    assert user.x1 == 1
    with pytest.raises(AttributeError):
        assert user.x2


def test_automatically_spec_mock():
    user = create_autospec(User, spec_set=True, instance=True, username="batman")
    assert user.username == "batman"
    with pytest.raises(AttributeError):
        create_autospec(User, spec_set=True, instance=True, x1=1)
    with pytest.raises(AttributeError):
        assert user.x2
    with pytest.raises(TypeError):
        user()  # raises exception because instance=True


# Doesn't work
# @patch("users.models.User", autospec=True)
# def test_automatically_define_mock_spec_with_patch(User):
#     user = User(username="batman")
#     assert user.username == "batman"
