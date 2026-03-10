from django.db import models
from .fields import UpperCaseCharField
from django.contrib.auth.models import AbstractUser


class Post(models.Model):
    """Model representing a blog post
    """

    title = UpperCaseCharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def count_comments(self) -> int:
        """Return the number of comments related to this post
        """
        return self.comments.count()

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    """Model representing a comment on a post
    """

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Comment for {self.post.title}"


class CustomUser(AbstractUser):
    """Custom user model with additional phone number field
    """

    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    def __str__(self) -> str:
        return self.username


class UpperCaseCharField(models.CharField):
    """Custom CharField that automatically converts string values to uppercase before saving
    """

    def pre_save(self, model_instance, add) -> None:
        """Prepare the value before saving to the database
        """
        value = super().pre_save(model_instance, add)
        if value:
            value = value.upper()
            setattr(model_instance, self.attname, value)
        return value


class Tag(models.Model):
    """Model representing a tag (stored in uppercase automatically)
    """
    name = UpperCaseCharField(max_length=50)

    def __str__(self) -> str:
        return self.name
