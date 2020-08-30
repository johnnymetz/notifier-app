from django.urls import include, path

from rest_framework.routers import DefaultRouter

from notifier.views import FriendViewset
from users.views import EmailMock, SeedQaUser, UserDetailView

router = DefaultRouter()
router.register("friends", FriendViewset)

urlpatterns = [
    path("", include(router.urls)),
    path("user/", UserDetailView.as_view(), name="user-detail"),
    path("user/email-mock/", EmailMock.as_view()),
    path("seed/qa-user/", SeedQaUser.as_view(), name="seed-qa-user"),
]
