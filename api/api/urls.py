import os

from django.contrib import admin
from django.urls import include, path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

# from .swagger import schema_view
from .views import Welcome

urlpatterns = [
    path(f"{os.environ.get('ADMIN_URL', 'admin')}/", admin.site.urls),
    path("", Welcome.as_view()),
    path("api/", include("notifier.urls")),
    # JWT token
    path("api/token/", TokenObtainPairView.as_view(), name="jwt-create"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="jwt-verify"),
    # # documentation
    # path("api/docs/", schema_view.with_ui("swagger")),
]
