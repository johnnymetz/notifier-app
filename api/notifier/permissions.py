from rest_framework.permissions import BasePermission, IsAuthenticated


class IsOwner(IsAuthenticated):
    """Only allow owners of an object to view and edit it."""

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


class IsCypress(BasePermission):
    def has_permission(self, request, view):
        return request.data.get("auth") == "Cypress789"

    def has_object_permission(self, request, view, obj):
        return request.data.get("auth") == "Cypress789"
