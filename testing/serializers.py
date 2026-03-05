from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Task

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model
    """

    class Meta:
        model = User
        fields = ["username", "email"]


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task model
    """

    user = UserSerializer()

    class Meta:
        model = Task
        fields = ["title", "description", "due_date", "user"]

    def validate_due_date(self, value) -> bool:
        """Validate that due_date is not in the past
        """
        if value < timezone.now().date():
            raise serializers.ValidationError(
                "Date cannot be in the past."
            )
        return value
