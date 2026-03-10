from django import template
from ..models import Post

register = template.Library()


@register.simple_tag
def total_posts() -> int:
    """custom tag: post count
    """
    return Post.objects.count()


@register.filter(name='truncate_words')
def truncate_words(value: str, num: int) -> str:
    """Custom filter: truncates text to a specified number of words
    """
    words = value.split()
    if len(words) > num:
        return ' '.join(words[:num]) + "..."
    return value
