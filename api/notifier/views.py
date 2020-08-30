from rest_framework import viewsets

from notifier.models import Friend
from notifier.permissions import IsOwner
from notifier.serializers import FriendSerializer


class FriendViewset(viewsets.ModelViewSet):
    # TODO: remove friend-list view
    queryset = Friend.objects.all()
    serializer_class = FriendSerializer
    permission_classes = (IsOwner,)
