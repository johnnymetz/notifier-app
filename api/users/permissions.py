from rest_framework.permissions import BasePermission


class IsCypress(BasePermission):
    def has_permission(self, request, view):
        return request.data.get("auth") == "Cypress789"

    def has_object_permission(self, request, view, obj):
        return request.data.get("auth") == "Cypress789"
