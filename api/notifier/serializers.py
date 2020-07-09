from django.contrib.auth.models import User

from rest_framework import serializers

from notifier.models import Friend


class FriendSerializer(serializers.ModelSerializer):
    birthday = serializers.CharField(source="birthday_display")
    # user = serializers.HyperlinkedRelatedField(view_name="user-detail", read_only=True)

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
    friends = FriendSerializer(many=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "friends")
