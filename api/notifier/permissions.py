from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Custom permission to only allow owners of an object to view and edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read/Write permissions are only allowed to the owner.
        return obj.user == request.user
