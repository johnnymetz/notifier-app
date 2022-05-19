import logging

import rollbar

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
        response = self.get_response(request)
        access_control_allow_origin = response.headers.get(
            "Access-Control-Allow-Origin"
        )

        if not access_control_allow_origin:
            important_request_headers = {
                header: request.META.get(header) for header in REQUEST_HEADERS
            }
            rollbar.report_message(
                f"Response has no 'Access-Control-Allow-Origin' header, which "
                f"means it will be blocked by CORS policy. The request has the "
                f"following headers: {important_request_headers}"
            )

        return response
