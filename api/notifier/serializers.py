from django.contrib.auth.models import User

from rest_framework import serializers

from notifier.helpers import get_friends_with_birthday_within
from notifier.models import Friend


class FriendSerializer(serializers.ModelSerializer):
    birthday = serializers.CharField(source="birthday_display")

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
