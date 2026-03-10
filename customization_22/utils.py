from .models import Post


def get_latest_posts(limit=5) -> list:
    """Retrieve the latest posts using a raw SQL query via Django ORM
    """
    return Post.objects.raw(
        "SELECT * FROM customization_22_post ORDER BY created_at DESC LIMIT %s", [limit]
    )
