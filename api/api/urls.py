from django.conf import settings
from django.contrib import admin
from django.urls import path

from .views import welcome

urlpatterns = [
    path(f"{settings.ADMIN_URL}/", admin.site.urls),
    path("", welcome)
    # path("", include("notifier.urls")),
]
