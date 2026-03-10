from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comment


@receiver(post_save, sender=Comment)
def comment_created(sender, instance, created, **kwargs) -> None:
    """Signal handler triggered when a new Comment is created
    """
    if created:
        print(f"New comment for post '{instance.post.title}': {instance.text}")
