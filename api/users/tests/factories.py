from django.contrib.auth import get_user_model

import factory

User = get_user_model()

TEST_PASSWORD = "pw123"


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n + 1}@email.com")
    password = TEST_PASSWORD

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        # The default would use `manager.create(*args, **kwargs)`
        return manager.create_user(*args, **kwargs)
