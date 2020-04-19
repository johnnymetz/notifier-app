from django.urls import include, path
from notifier.views import FriendViewset, UserViewset, email_testing
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("users", UserViewset)
router.register("friends", FriendViewset)

urlpatterns = [
    path("", include(router.urls)),
    path("testing/", email_testing),
]
