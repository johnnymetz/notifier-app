from django.contrib.auth.models import User
from django.shortcuts import render
from notifier.models import Friend
from notifier.serializers import FriendSerializer, UserSerializer
from rest_framework import viewsets


class UserViewset(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class FriendViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Friend.objects.order_by("date_of_birth")
    serializer_class = FriendSerializer


def email_testing(request):
    friends = Friend.objects.all()[:5]
    context = {"friends": friends}
    return render(request, "notifier/birthdays-email.html", context)
