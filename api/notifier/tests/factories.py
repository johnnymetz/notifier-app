import datetime

import factory
from django.contrib.auth.models import User
from notifier.models import Friend


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"User{n + 1}")


class FriendFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Friend

    user = factory.SubFactory(UserFactory)
    first_name = factory.Sequence(lambda n: f"Friend{n + 1}")
    last_name = factory.Faker("last_name")
    date_of_birth = datetime.datetime(2000, 1, 1)

    @factory.post_generation
    def finish(self, create, extended):
        if not create:
            return
        self.clean()
