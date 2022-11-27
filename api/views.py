from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class Welcome(APIView):
    permission_classes = (AllowAny,)

    def get(self, *args, **kwargs):
        return Response({"message": "Welcome to the Notifier API."})
