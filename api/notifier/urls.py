from django.urls import include, path

from rest_framework.routers import DefaultRouter

from notifier.views import FriendViewset, UserViewset, email_testing

router = DefaultRouter()
router.register("users", UserViewset)
router.register("friends", FriendViewset)

urlpatterns = [
    path("", include(router.urls)),
    path("testing/<username>/", email_testing),
]
