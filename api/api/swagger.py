# https://drf-yasg.readthedocs.io/en/stable/readme.html#quickstart
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title="Notifier API", default_version="1.0.0", description="Notifier API"
    ),
    public=True,
    permission_classes=(AllowAny,),
)
