import os

from django.contrib import admin
from django.urls import include, path

from .views import welcome

urlpatterns = [
    path(f"{os.environ.get('ADMIN_URL', 'admin')}/", admin.site.urls),
    path("", welcome),
    path("api/", include("notifier.urls")),
]
