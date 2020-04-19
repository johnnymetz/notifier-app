from django.apps import AppConfig


class NotifierConfig(AppConfig):
    name = "notifier"

    def ready(self):
        # register signals
        import notifier.signals
