import datetime

from django.contrib.auth.models import User

from rest_framework import serializers

from notifier.constants import UNKNOWN_YEAR
from notifier.models import Friend
from notifier.user_helpers import get_friends_with_birthday_within

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


class UserSerializer(serializers.ModelSerializer):
    all_friends = serializers.SerializerMethodField()
    upcoming_friends = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "username", "email", "all_friends", "upcoming_friends")

    @staticmethod
    def get_all_friends(obj):
        return FriendSerializer(obj.friends.all(), many=True).data

    @staticmethod
    def get_upcoming_friends(obj):
        friends_with_bday_upcoming = get_friends_with_birthday_within(user=obj, days=5)
        return FriendSerializer(friends_with_bday_upcoming, many=True).data
