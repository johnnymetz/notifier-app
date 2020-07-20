import datetime

from django.contrib.auth.models import User

import factory

from notifier.models import Friend


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"User{n + 1}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@email.com")
    password = "pw123"

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        # The default would use `manager.create(*args, **kwargs)`
        return manager.create_user(*args, **kwargs)


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
