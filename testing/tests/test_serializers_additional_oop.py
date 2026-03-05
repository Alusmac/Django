from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from testing.serializers import TaskSerializer


class SerializerAdditionalTest(TestCase):
    """Test suite for validation
    """

    def test_additional_valid_data(self) -> None:
        """Serializer should be valid when correct additional user data is provided
        """
        data = {
            "title": "Test",
            "description": "Desc",
            "due_date": timezone.now().date() + timedelta(days=2),
            "user": {
                "username": "testuser",
                "email": "test@test.com",
            },
        }

        serializer = TaskSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_additional_invalid_user(self) -> None:
        """Serializer should fail when additional user data is invalid
        """
        data = {
            "title": "Test",
            "description": "Desc",
            "due_date": timezone.now().date() + timedelta(days=2),
            "user": {
                "username": "",
                "email": "invalid",
            },
        }

        serializer = TaskSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("user", serializer.errors)
