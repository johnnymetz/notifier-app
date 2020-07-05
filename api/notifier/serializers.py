from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.settings import api_settings

from notifier.models import Friend


class UserSerializer(serializers.ModelSerializer):
    friends = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "username", "email", "friends")

    def get_friends(self, obj):
        paginator = api_settings.DEFAULT_PAGINATION_CLASS()
        page = paginator.paginate_queryset(obj.friends.all(), self.context["request"])
        serializer = FriendSerializer(
            page, many=True, context={"request": self.context["request"]}
        )
        paginated_data = paginator.get_paginated_response(serializer.data).data
        return paginated_data


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
