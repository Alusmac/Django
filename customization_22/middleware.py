import logging
from typing import Callable
from django.http import HttpRequest, HttpResponse

logger = logging.getLogger("django")


class CustomHeaderMiddleware:
    """Middleware that adds a custom header 'X-App-Version' to all responses
    """

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        """Initialize the middleware with the get_response callable
        """
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Process the request and add custom header to the response
        """
        response = self.get_response(request)
        response["X-App-Version"] = "1.0.0"
        return response


class RequestCounterMiddleware:
    """Middleware that counts the number of requests and logs them
    """

    request_count: int = 0

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        """Initialize the middleware with the get_response callable
        """
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Process the request, increment counter, log it, and add it as a header
        """
        RequestCounterMiddleware.request_count += 1
        logger.info(f"Request #{RequestCounterMiddleware.request_count}: {request.path}")

        response = self.get_response(request)
        response["X-Request-Number"] = str(RequestCounterMiddleware.request_count)
        return response
