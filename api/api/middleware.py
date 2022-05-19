import logging

import rollbar
from rest_framework.response import Response

logger = logging.getLogger(__name__)


REQUEST_HEADERS = [
    "HTTP_ORIGIN",
    "HTTP_REFERER",
    "HTTP_ACCESS_CONTROL_REQUEST_METHOD",
    "HTTP_ACCESS_CONTROL_REQUEST_HEADERS",
]


class ReportFailedCORSPreflightMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response: Response = self.get_response(request)
        access_control_allow_origin = response.headers.get(
            "Access-Control-Allow-Origin"
        )

        if not access_control_allow_origin:
            rollbar.report_message(
                "Response has no 'Access-Control-Allow-Origin' header, which "
                "means it will be blocked by CORS policy"
            )

        return response
