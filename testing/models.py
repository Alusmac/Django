from django.db import models
from django.conf import settings


class Task(models.Model):
    """Task model represents a user task with a title,
    optional description, deadline, and owner
    """
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title
