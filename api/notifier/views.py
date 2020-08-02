from django.contrib.auth.models import User
from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from notifier.models import Friend
from notifier.permissions import IsOwner
from notifier.serializers import FriendSerializer, UserSerializer
from notifier.user_helpers import get_birthday_email_context


class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        # import time
        # time.sleep(3)
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class FriendViewset(viewsets.ModelViewSet):
    queryset = Friend.objects.all()
    serializer_class = FriendSerializer
    permission_classes = (IsAuthenticated, IsOwner)


class EmailMock(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = User.objects.get(username=request.user.username)
        context = get_birthday_email_context(user)
        return render(request, "notifier/birthdays-email.html", context)
