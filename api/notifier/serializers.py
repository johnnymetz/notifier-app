from django.contrib.auth.models import User

from rest_framework import serializers

from notifier.models import Friend

# from rest_framework.settings import api_settings


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
    # friends = serializers.SerializerMethodField()
    friends = FriendSerializer(many=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "friends")

    # def get_friends(self, obj):
    #     paginator = api_settings.DEFAULT_PAGINATION_CLASS()
    #     page = paginator.paginate_queryset(obj.friends.all(), self.context["request"])
    #     serializer = FriendSerializer(
    #         page, many=True, context={"request": self.context["request"]}
    #     )
    #     paginated_data = paginator.get_paginated_response(serializer.data).data
    #     return paginated_data
