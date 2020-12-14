import datetime

from rest_framework import serializers

from notifier.constants import UNKNOWN_YEAR
from notifier.models import Event


class DateField(serializers.Field):
    def to_representation(self, value):
        return {
            "year": None if value.year == UNKNOWN_YEAR else value.year,
            "month": value.month,
            "day": value.day,
        }

    def to_internal_value(self, data):
        try:
            return datetime.date(
                int(data.get("year", UNKNOWN_YEAR)),
                int(data["month"]),
                int(data["day"]),
            )
        except Exception:
            raise serializers.ValidationError("Error parsing birth date")


class EventSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    annual_date = DateField()

    class Meta:
        model = Event
        fields = ("id", "user", "name", "annual_date", "type", "age")

    def create(self, validated_data):
        return self.Meta.model.objects.create(
            **validated_data, user=self.context["request"].user
        )

    def update(self, instance, validated_data):
        try:
            instance.name = validated_data.get("name", instance.name)
            instance.annual_date = validated_data.get(
                "annual_date", instance.annual_date
            )
            instance.type = validated_data.get("type", instance.type)
            instance.save()
            return instance
        except ValueError as e:
            raise serializers.ValidationError(e)
