import logging
import time

from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from notifier.exceptions import NotifierError
from users.permissions import IsCypress

logger = logging.getLogger(__name__)


class ThrowError(APIView):
    permission_classes = (IsCypress,)

    def post(self, *args, **kwargs):
        raise NotifierError("Bad news bears")


DEFAULT_TIMEOUT = 15


class TimeoutView(APIView):
    permission_classes = (IsCypress,)

    def post(self, request, *args, **kwargs):
        seconds = request.data.get("seconds", DEFAULT_TIMEOUT)

        try:
            seconds = int(seconds)
        except ValueError:
            raise serializers.ValidationError(f"Invalid seconds input: {seconds}")

        for i in range(seconds):
            logger.info(f"Slept for {i + 1}/{seconds} seconds")
            time.sleep(1)

        return Response(status=status.HTTP_204_NO_CONTENT)
