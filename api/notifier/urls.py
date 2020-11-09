from django.urls import include, path

from rest_framework.routers import DefaultRouter

from notifier.views import EmailMock, FriendViewset
from users.views import SeedQaUser

router = DefaultRouter()
router.register("friends", FriendViewset)

urlpatterns = [
    path("", include(router.urls)),
    path("seed/qa-user/", SeedQaUser.as_view(), name="seed-qa-user"),
    path("user/email-mock/<email>/", EmailMock.as_view()),
]
