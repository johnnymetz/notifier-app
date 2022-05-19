import logging

# from corsheaders.middleware import (
#     ACCESS_CONTROL_ALLOW_CREDENTIALS,
#     ACCESS_CONTROL_ALLOW_HEADERS,
#     ACCESS_CONTROL_ALLOW_METHODS,
#     ACCESS_CONTROL_ALLOW_ORIGIN,
#     ACCESS_CONTROL_EXPOSE_HEADERS,
# )

logger = logging.getLogger(__name__)


REQUEST_HEADERS = [
    "HTTP_ORIGIN",
    "HTTP_REFERER",
    "HTTP_ACCESS_CONTROL_REQUEST_METHOD",
    "HTTP_ACCESS_CONTROL_REQUEST_HEADERS",
    # "HTTP_CACHE_CONTROL",
]

# RESPONSE_HEADERS = [
#     ACCESS_CONTROL_ALLOW_ORIGIN,
#     ACCESS_CONTROL_EXPOSE_HEADERS,
#     ACCESS_CONTROL_ALLOW_CREDENTIALS,
#     ACCESS_CONTROL_ALLOW_HEADERS,
#     ACCESS_CONTROL_ALLOW_METHODS,
# ]

RESPONSE_HEADERS = [
    "Access-Control-Allow-Origin",
    "Access-Control-Allow-Methods",
    "Access-Control-Allow-Headers",
    "Access-Control-Expose-Headers",
    "Access-Control-Response-Headers",
    "Access-Control-Max-Age",
    "Cache-Control",
]


class LogFailedCORSPreflightMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # method = request.method
        # print(method)
        #
        # if method == "OPTIONS":
        #     for header in REQUEST_HEADERS:
        #         print(f"{header}, {request.META.get(header)}")

        response = self.get_response(request)

        # if method == "OPTIONS":
        #     # response.headers["Cache-Control"] = "no-cache, no-store"
        #     for header in RESPONSE_HEADERS:
        #         print(f"{header}: {response.headers.get(header)}")

        access_control_allow_origin = response.headers.get(
            "Access-Control-Allow-Origin"
        )

        if not access_control_allow_origin:
            important_request_headers = {
                header: request.META.get(header) for header in REQUEST_HEADERS
            }
            logger.error(
                f"Response has no 'Access-Control-Allow-Origin' header, which "
                f"means it will be blocked by CORS policy. The request has the "
                f"following headers: {important_request_headers}"
            )

        return response
