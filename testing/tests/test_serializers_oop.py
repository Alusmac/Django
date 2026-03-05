from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from testing.serializers import TaskSerializer


class TaskSerializerTest(TestCase):
    """Test suite for validation
    """

    def test_serializer_valid_data(self) -> None:
        """Checking the serializer's validity with correct data
        """
        data = {
            "title": "Test task",
            "description": "Test description",
            "due_date": timezone.now().date() + timedelta(days=2),
            "user": {
                "username": "testuser",
                "email": "test@example.com"
            }
        }
        serializer = TaskSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_missing_title(self) -> None:
        """Test that serializer returns error when required field 'title' is missing
        """
        data = {
            "description": "Test description",
            "due_date": timezone.now().date() + timedelta(days=2),
        }
        serializer = TaskSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)

    def test_serializer_due_date_in_past(self) -> None:
        """Test that serializer rejects due_date in the past
        """
        data = {
            "title": "Test task",
            "description": "Test description",
            "due_date": timezone.now().date() - timedelta(days=1),
        }
        serializer = TaskSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("due_date", serializer.errors)
