from .models import Post
from django.http import HttpRequest


def latest_posts(request: HttpRequest) -> dict:
    """Context processor to provide the latest 5 posts for templates
    """
    return {
        "latest_posts": Post.objects.order_by('-created_at')[:5]
    }
