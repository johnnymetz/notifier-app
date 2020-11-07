import os

from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.permissions import IsCypress
from users.serializers import UserSerializer

User = get_user_model()


class SeedQaUser(APIView):
    permission_classes = (IsCypress,)

    def post(self, request, *args, **kwargs):
        qa_user_email = os.environ.get("QA_USER_EMAIL")
        qa_user_password = os.environ.get("QA_USER_PASSWORD")

        if not qa_user_email or not qa_user_password:
            return Response("Missing qa credentials", status=status.HTTP_201_CREATED)

        try:
            User.objects.get(email=qa_user_email).delete()
        except User.DoesNotExist:
            pass
        qa_user = User.objects.create(email=qa_user_email)
        qa_user.set_password(qa_user_password)
        qa_user.save()
        _ = qa_user.add_friends_from_csv(
            filename=f"{settings.BASE_DIR}/notifier/data/qa_friends.csv"
        )
        serializer = UserSerializer(qa_user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
