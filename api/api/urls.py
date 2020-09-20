import os

from django.contrib import admin
from django.urls import include, path

# from .swagger import schema_view
from .views import Welcome

urlpatterns = [
    path(f"{os.environ.get('ADMIN_URL', 'admin')}/", admin.site.urls),
    path("", Welcome.as_view()),
    path("api/", include("notifier.urls")),
    path("api/auth/", include("djoser.urls")),
    path("api/auth/", include("djoser.urls.jwt")),
    # # documentation
    # path("api/docs/", schema_view.with_ui("swagger")),
]
