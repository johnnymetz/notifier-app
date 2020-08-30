import datetime

import factory

from notifier.models import Friend
from users.tests.factories import UserFactory


class FriendFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Friend

    user = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: f"Friend{n + 1}")
    date_of_birth = datetime.date(2000, 1, 1)

    @factory.post_generation
    def finish(self, create, extended):
        if not create:
            return
        self.clean()
