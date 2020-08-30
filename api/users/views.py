import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import render

from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.permissions import IsCypress
from users.serializers import UserSerializer

User = get_user_model()


class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        # import time
        # time.sleep(3)
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class SeedQaUser(APIView):
    permission_classes = (IsCypress,)

    def post(self, request, *args, **kwargs):
        qa_user_email = os.environ.get("QA_USER_EMAIL")
        if not qa_user_email:
            return Response("No email set", status=status.HTTP_201_CREATED)

        try:
            User.objects.get(email=qa_user_email).delete()
        except User.DoesNotExist:
            pass
        qa_user = User.objects.create(email=qa_user_email)
        qa_user.set_password("qa")
        qa_user.save()
        _ = qa_user.add_friends_from_csv(
            filename=f"{settings.BASE_DIR}/notifier/data/qa_friends.csv"
        )
        serializer = UserSerializer(qa_user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class EmailMock(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = User.objects.get(email=request.user.email)
        context = user.get_birthday_email_context()
        return render(request, "notifier/birthdays-email.html", context)
