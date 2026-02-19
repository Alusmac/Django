from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone
from datetime import timedelta


class Profile(models.Model):
    """User profile information
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"Profile of {self.user.username}"


class Category(models.Model):
    """Category for ads information
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def active_ads_count(self) -> int:
        """Number of active ads
        """
        return self.ads.filter(is_active=True).count()

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Ad(models.Model):
    """Ad information
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='ads'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='ads'
    )

    def short_description(self) -> str:
        """Get the first 100 characters of the ad description
        """
        return self.description[:100]

    def deactivate_if_expired(self) -> None:
        """Deactivate the ad if it is older than 30 days
        """
        if self.created_at <= timezone.now() - timedelta(days=30):
            self.is_active = False
            self.save()

    def comments_count(self) -> int:
        """Count the number of comments for this ad
        """
        return self.comments.count()

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    """Comment on the announcement
    """
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    ad = models.ForeignKey(
        Ad,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    def __str__(self) -> str:
        return f"Comment by {self.user.username}"
