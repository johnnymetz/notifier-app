from django.contrib.auth import get_user_model

import factory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    email = factory.Sequence(lambda n: f"user{n + 1}@email.com")
    password = "pw123"

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        # The default would use `manager.create(*args, **kwargs)`
        return manager.create_user(*args, **kwargs)
