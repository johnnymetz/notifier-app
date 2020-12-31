import os

from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import include, path

# from .swagger import schema_view
from .views import Welcome

urlpatterns = [
    path(f"{os.environ.get('ADMIN_URL', 'admin')}/", admin.site.urls),
    path("", Welcome.as_view(), name="welcome"),
    path("api/", include("notifier.urls")),
    path("api/auth/", include("djoser.urls")),
    path("api/auth/", include("djoser.urls.jwt")),
    # # documentation
    # path("api/docs/", schema_view.with_ui("swagger")),
    path("silk/", include("silk.urls", namespace="silk")),
    path(
        settings.LOGIN_URL.removeprefix("/"),
        LoginView.as_view(
            template_name="admin/login.html",
            extra_context={"site_header": "Silk Debugging"},
        ),
    ),
]
