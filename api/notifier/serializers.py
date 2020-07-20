import datetime

from django.contrib.auth.models import User

from rest_framework import serializers

from notifier.constants import UNKNOWN_YEAR
from notifier.helpers import get_friends_with_birthday_within
from notifier.models import Friend


class YearField(serializers.IntegerField):
    def to_representation(self, value):
        year = int(value)
        return None if year == UNKNOWN_YEAR else year


class FriendSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    birthday_year = YearField(source="date_of_birth.year", required=False)
    birthday_month = serializers.IntegerField(source="date_of_birth.month")
    birthday_day = serializers.IntegerField(source="date_of_birth.day")

    class Meta:
        model = Friend
        fields = (
            "id",
            "user",
            "first_name",
            "last_name",
            "birthday_year",
            "birthday_month",
            "birthday_day",
            "age",
        )

    def validate(self, data):
        date_or_birth = data.pop("date_of_birth")
        data["date_of_birth"] = datetime.date(
            date_or_birth.get("year", UNKNOWN_YEAR),
            date_or_birth["month"],
            date_or_birth["day"],
        )
        return data

    def create(self, validated_data):
        return self.Meta.model.objects.create(
            **validated_data, user=self.context["request"].user
        )

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.date_of_birth = validated_data.get(
            "date_of_birth", instance.date_of_birth
        )
        instance.save()
        return instance


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
