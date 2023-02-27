from django.conf import settings

from rest_framework.permissions import BasePermission


class IsCypress(BasePermission):
    def has_permission(self, request, view):
        auth = request.data.get("auth")
        return auth and auth == settings.CYPRESS_AUTH_SECRET

    def has_object_permission(self, request, view, obj):
        auth = request.data.get("auth")
        return auth and auth == settings.CYPRESS_AUTH_SECRET
