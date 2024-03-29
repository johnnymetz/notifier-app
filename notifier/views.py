from django.shortcuts import render

from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from notifier.models import Event
from notifier.permissions import IsOwner
from notifier.serializers import EventSerializer
from users.models import User


class ModelViewSetWithoutList(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()` and `destroy()` actions.

    Note no `list()`.
    """

    pass


class EventViewset(ModelViewSetWithoutList):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (IsOwner,)


class EventsEmailView(APIView):
    def get(self, request, email, *args, **kwargs):
        user = User.objects.get(email=email)
        context = user.get_events_email_context()
        return render(request, "notifier/events-email.html", context)
