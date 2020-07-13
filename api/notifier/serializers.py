import datetime

from django.contrib.auth.models import User

from rest_framework import serializers

from notifier.constants import BIRTHDAY_FORMAT, UNKNOWN_YEAR
from notifier.helpers import get_friends_with_birthday_within
from notifier.models import Friend


class FriendSerializer(serializers.ModelSerializer):
    birthday = serializers.DateField(
        source="date_of_birth",
        format=BIRTHDAY_FORMAT,
        input_formats=[BIRTHDAY_FORMAT, "iso-8601"],
    )
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Friend
        fields = (
            "id",
            "user",
            "first_name",
            "last_name",
            "birthday",
            "age",
        )

    def validate_birthday(self, value: datetime.date):
        # Year defaults to 1900 if none is sent in payload;
        # this may be a better UNKNOWN_YEAR value
        if value.year == 1900:
            value = value.replace(year=UNKNOWN_YEAR)
        return value

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
