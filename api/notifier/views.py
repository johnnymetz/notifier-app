from django.contrib.auth import get_user_model
from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from notifier.models import Friend
from notifier.permissions import IsOwner
from notifier.serializers import FriendSerializer

User = get_user_model()


class FriendViewset(viewsets.ModelViewSet):
    # TODO: remove get friend-list view
    queryset = Friend.objects.all()
    serializer_class = FriendSerializer
    permission_classes = (IsOwner,)


class EmailMock(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = User.objects.get(email=request.user.email)
        context = user.get_birthday_email_context()
        return render(request, "notifier/birthdays-email.html", context)
