from django.contrib.auth.models import User
from notifier.models import Friend
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ("url", "id", "username", "friends")


class FriendSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Friend
        fields = (
            "url",
            "user",
            "first_name",
            "last_name",
            "date_of_birth",
            "month",
            "day",
        )
