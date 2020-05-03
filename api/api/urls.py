from django.contrib import admin
from django.urls import path

from .views import welcome

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", welcome)
    # path("", include("notifier.urls")),
]
