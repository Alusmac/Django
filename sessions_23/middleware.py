from django.core.cache import cache
from django.http import HttpRequest, HttpResponse
from django.utils.deprecation import MiddlewareMixin


class AnonymousPageCacheMiddleware(MiddlewareMixin):
    """Middleware to cache full pages for anonymous users
    """

    def process_request(self, request: HttpRequest) -> HttpResponse | None:
        """Check if a cached response exists for the anonymous user
        """
        if request.user.is_anonymous:
            key = f"anon_page_cache:{request.path}"
            response = cache.get(key)
            if response:
                return response

    def process_response(self, request: HttpRequest, response: HttpResponse) -> HttpResponse:
        """Cache the response for anonymous users
        """
        if request.user.is_anonymous:
            key = f"anon_page_cache:{request.path}"
            cache.set(key, response, 60 * 5)
        return response
