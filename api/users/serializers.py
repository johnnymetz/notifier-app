from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    all_events = serializers.SerializerMethodField()
    events_today = serializers.SerializerMethodField()
    events_upcoming = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "is_subscribed",
            "all_events",
            "events_today",
            "events_upcoming",
        )

    @staticmethod
    def get_all_events(obj):
        from notifier.serializers import EventSerializer

        return EventSerializer(obj.events.all(), many=True).data

    @staticmethod
    def get_events_today(obj):
        from notifier.serializers import EventSerializer

        events_today = obj.get_events_today()
        return EventSerializer(events_today, many=True).data

    @staticmethod
    def get_events_upcoming(obj):
        from notifier.serializers import EventSerializer

        events_upcoming = obj.get_events_upcoming()
        return EventSerializer(events_upcoming, many=True).data
