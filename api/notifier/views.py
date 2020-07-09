from django.contrib.auth.models import User
from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from notifier.helpers import get_birthday_email_context
from notifier.models import Friend
from notifier.serializers import FriendSerializer, UserSerializer


class UserViewset(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)


class FriendViewset(viewsets.ModelViewSet):
    queryset = Friend.objects.all()
    serializer_class = FriendSerializer


def email_testing(request, username):
    user = User.objects.get(username=username)
    context = get_birthday_email_context(user)
    return render(request, "notifier/birthdays-email.html", context)
