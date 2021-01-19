import datetime

import factory

from notifier.models import Event
from users.tests.factories import UserFactory


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event

    user = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: f"Event{n + 1}")
    annual_date = datetime.date(2000, 1, 1)
    type = Event.EventType.BIRTHDAY  # noqa

    @factory.post_generation
    def finish(self, create, extended):
        if not create:
            return
        self.clean()
