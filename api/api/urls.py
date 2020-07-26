import os

from django.contrib import admin
from django.urls import include, path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import Welcome

urlpatterns = [
    path(f"{os.environ.get('ADMIN_URL', 'admin')}/", admin.site.urls),
    path("", Welcome.as_view()),
    path("api/", include("notifier.urls")),
    # JWT token
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
