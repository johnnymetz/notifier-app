from rest_framework.permissions import IsAuthenticated


class IsOwner(IsAuthenticated):
    """Only allow owners of an object to view and edit it."""

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user
