import logging
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

logger = logging.getLogger(__name__)


class AccessLogMiddleware:
    """Middleware for logging access to protected dashboard routes
    """

    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Process the incoming HTTP request
        """
        if request.path.startswith('/dashboard'):
            logger.info(f"User {request.user} accessed {request.path}")
        return self.get_response(request)


class ErrorHandlingMiddleware:
    """Middleware for handling HTTP error responses
    """

    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Process the request and handle error responses
        """
        response = self.get_response(request)
        if response.status_code == 404:
            return render(request, 'security/404.html', status=404)
        if response.status_code == 500:
            return render(request, 'security/500.html', status=500)
        return response
