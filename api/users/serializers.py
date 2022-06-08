from newrelic.agent import record_custom_metric
from rest_framework import serializers

from api.telemetry import metrics
from users.models import User


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
        from notifier.helpers import sort_events_by_yearless_date_starting_at_today
        from notifier.serializers import EventSerializer

        all_events = sort_events_by_yearless_date_starting_at_today(obj.events.all())
        record_custom_metric(metrics.USER_EVENTS_ALL, len(all_events))

        return EventSerializer(all_events, many=True).data

    @staticmethod
    def get_events_today(obj):
        from notifier.serializers import EventSerializer

        events_today = obj.get_events_today()
        record_custom_metric(metrics.USER_EVENTS_TODAY, len(events_today))

        return EventSerializer(events_today, many=True).data

    @staticmethod
    def get_events_upcoming(obj):
        from notifier.serializers import EventSerializer

        events_upcoming = obj.get_events_upcoming()
        record_custom_metric(metrics.USER_EVENTS_UPCOMING, len(events_upcoming))

        return EventSerializer(events_upcoming, many=True).data
