import pytest
from datetime import timedelta
from django.utils import timezone
from testing.serializers import TaskSerializer


@pytest.mark.django_db
def test_additional_serializer_valid_data() -> None:
    """Serializer should be valid when correct additional user data is provided
    """
    data = {
        "title": "Test task",
        "description": "Test description",
        "due_date": timezone.now().date() + timedelta(days=2),
        "user": {
            "username": "testuser",
            "email": "test@example.com",
        },
    }

    serializer = TaskSerializer(data=data)

    assert serializer.is_valid(), serializer.errors


@pytest.mark.django_db
def test_additional_serializer_invalid_user_data() -> None:
    """Serializer should fail when additional user data is invalid
    """
    data = {
        "title": "Test task",
        "description": "Test description",
        "due_date": timezone.now().date() + timedelta(days=2),
        "user": {
            "username": "",
            "email": "not-an-email",
        },
    }

    serializer = TaskSerializer(data=data)

    assert not serializer.is_valid()
    assert "user" in serializer.errors


@pytest.mark.django_db
def test_additional_serializer_invalid_user() -> None:
    """Serializer should fail if additional user is missing
    """
    data = {
        "title": "Test task",
        "description": "Test description",
        "due_date": timezone.now().date() + timedelta(days=2),
    }

    serializer = TaskSerializer(data=data)

    assert not serializer.is_valid()
    assert "user" in serializer.errors.errors
