from django.urls import include, path

from rest_framework.routers import DefaultRouter

from notifier.views import EventsEmailView, EventViewset, ThrowError
from users.views import SeedQaUser

router = DefaultRouter()
router.register("events", EventViewset)

urlpatterns = [
    path("", include(router.urls)),
    path("seed/qa-user/", SeedQaUser.as_view(), name="seed-qa-user"),
    path("user/events-email/<email>/", EventsEmailView.as_view()),
    path("throw/", ThrowError.as_view()),
]
