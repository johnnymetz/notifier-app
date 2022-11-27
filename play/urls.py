from django.urls import path

from play.views import ThrowError, TimeoutView

urlpatterns = [
    path("throw/", ThrowError.as_view()),
    path("timeout/", TimeoutView.as_view()),
]
