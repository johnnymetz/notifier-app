from django.core.management import call_command

import pytest

from users.tests.factories import UserFactory


@pytest.mark.django_db
def test_email_group_of_users(mailoutbox):
    users = [
        UserFactory(),
        UserFactory(is_active=False),
        UserFactory(is_subscribed=False),
        UserFactory(is_active=False, is_subscribed=False),
        UserFactory(),
    ]
    call_command(
        "send_birthday_emails",
        *[u.email for u in users],
        users[0].email,  # duplicate is skipped
        "xxx@mail.com",  # non-existent is skipped
    )
    assert len(mailoutbox) == 2


@pytest.mark.django_db
def test_email_all_users(mailoutbox):
    UserFactory()
    UserFactory(is_active=False)
    UserFactory(is_subscribed=False)
    UserFactory(is_active=False, is_subscribed=False)
    UserFactory()
    call_command("send_birthday_emails", "*")
    assert len(mailoutbox) == 2
