from django.contrib.auth import get_user_model
from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.views import APIView

from notifier.models import Event
from notifier.permissions import IsOwner
from notifier.serializers import EventSerializer

User = get_user_model()


class EventViewset(viewsets.ModelViewSet):
    # TODO: remove get event-list view
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (IsOwner,)


class EmailMock(APIView):
    def get(self, request, email, *args, **kwargs):
        user = User.objects.get(email=email)
        context = user.get_email_context()
        return render(request, "notifier/events-email.html", context)
