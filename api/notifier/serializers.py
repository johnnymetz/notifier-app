import datetime

from rest_framework import serializers

from notifier.constants import UNKNOWN_YEAR
from notifier.models import Friend

# class YearField(serializers.IntegerField):
#     def to_representation(self, value):
#         year = int(value)
#         return None if year == UNKNOWN_YEAR else year


# class DateSerializer(serializers.Serializer):
#     year = YearField(required=False)
#     month = serializers.IntegerField()
#     day = serializers.IntegerField()
#
#     def validate(self, data):
#         try:
#             return datetime.date(
#                 data.get("year", UNKNOWN_YEAR), data["month"], data["day"]
#             )
#         except ValueError as e:
#             raise serializers.ValidationError(e)


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


class FriendSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    # date_of_birth = DateSerializer()
    date_of_birth = DateField()

    class Meta:
        model = Friend
        fields = ("id", "user", "name", "date_of_birth", "age")

    def create(self, validated_data):
        return self.Meta.model.objects.create(
            **validated_data, user=self.context["request"].user
        )

    def update(self, instance, validated_data):
        try:
            instance.name = validated_data.get("name", instance.name)
            instance.date_of_birth = validated_data.get(
                "date_of_birth", instance.date_of_birth
            )
            instance.save()
            return instance
        except ValueError as e:
            raise serializers.ValidationError(e)
