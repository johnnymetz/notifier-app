from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    all_friends = serializers.SerializerMethodField()
    upcoming_friends = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "email", "is_subscribed", "all_friends", "upcoming_friends")

    @staticmethod
    def get_all_friends(obj):
        from notifier.serializers import FriendSerializer

        return FriendSerializer(obj.friends.all(), many=True).data

    @staticmethod
    def get_upcoming_friends(obj):
        from notifier.serializers import FriendSerializer

        friends_with_bday_upcoming = obj.get_friends_with_birthday_within(days=5)
        return FriendSerializer(friends_with_bday_upcoming, many=True).data
