import datetime
import os
from types import SimpleNamespace

from django.contrib.auth import get_user_model
from django.utils import timezone

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.permissions import IsCypress
from users.serializers import UserSerializer

User = get_user_model()


class SeedQaUser(APIView):
    permission_classes = (IsCypress,)

    def _get_and_delete_qa_users(self):
        qa_user_email1 = os.environ.get("QA_USER_EMAIL1")
        qa_user_email2 = os.environ.get("QA_USER_EMAIL2")
        qa_user_password = os.environ.get("QA_USER_PASSWORD")

        if not qa_user_email1 or not qa_user_email2 or not qa_user_password:
            return Response(
                "Missing qa credentials", status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        try:
            User.objects.filter(email__in=[qa_user_email1, qa_user_email2]).delete()
        except User.DoesNotExist:
            pass

        return SimpleNamespace(
            email1=qa_user_email1, email2=qa_user_email2, password=qa_user_password
        )

    def post(self, request, *args, **kwargs):
        from notifier.constants import UNKNOWN_YEAR
        from notifier.models import Event

        qa_creds = self._get_and_delete_qa_users()

        qa_user = User.objects.create(email=qa_creds.email1)
        qa_user.set_password(qa_creds.password)
        qa_user.save()

        # create user events
        today = timezone.localdate()
        if request.data.get("dataset") == "relative":
            ten_years_ago = today.year - 10
            dataset = [
                # today
                (today.replace(year=ten_years_ago), Event.EventType.BIRTHDAY),
                (today.replace(year=UNKNOWN_YEAR), Event.EventType.BIRTHDAY),
                (today + datetime.timedelta(days=365), Event.EventType.OTHER),
                # tomorrow
                (today + datetime.timedelta(days=1), Event.EventType.OTHER),
                (
                    (today - datetime.timedelta(days=364)).replace(year=ten_years_ago),
                    Event.EventType.BIRTHDAY,
                ),
                # other days
                (today - datetime.timedelta(days=1), Event.EventType.BIRTHDAY),
                (today - datetime.timedelta(days=300), Event.EventType.BIRTHDAY),
                (today + datetime.timedelta(days=30), Event.EventType.OTHER),
                (
                    (today + datetime.timedelta(days=30)).replace(year=ten_years_ago),
                    Event.EventType.OTHER,
                ),
                (
                    (today + datetime.timedelta(days=120)).replace(year=UNKNOWN_YEAR),
                    Event.EventType.OTHER,
                ),
            ]
        else:
            dataset = [
                (datetime.date(1994, 1, 24), Event.EventType.BIRTHDAY),
                (datetime.date(1959, 3, 28), Event.EventType.BIRTHDAY),
                (datetime.date(1960, 11, 26), Event.EventType.BIRTHDAY),
                (datetime.date(1999, 12, 31), Event.EventType.HOLIDAY),
            ]

        for i, (date, _type) in enumerate(dataset):
            assert isinstance(date, datetime.date)
            Event.objects.get_or_create(
                user=qa_user, name=f"Event{i + 1}", annual_date=date, type=_type
            )

        serializer = UserSerializer(qa_user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        self._get_and_delete_qa_users()
        return Response(status=status.HTTP_204_NO_CONTENT)
