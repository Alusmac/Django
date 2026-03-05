import pytest
from django.utils import timezone
from datetime import timedelta
from testing.serializers import TaskSerializer


@pytest.mark.django_db
def test_serializer_valid_data() -> None:
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
    assert serializer.is_valid(), serializer.errors


@pytest.mark.django_db
def test_serializer_invalid_due_date() -> None:
    """Test that serializer rejects due_date in the past
    """
    data = {
        "title": "Test task",
        "description": "Test description",
        "due_date": timezone.now().date() - timedelta(days=1),
        "user": {
            "username": "testuser",
            "email": "test@example.com"
        }
    }

    serializer = TaskSerializer(data=data)

    assert not serializer.is_valid(), serializer.errors
    assert "due_date" in serializer.errors


@pytest.mark.django_db
def test_serializer_missing_title() -> None:
    """Test that serializer returns error when required field 'title' is missing
    """
    data = {
        "description": "Test description",
        "due_date": timezone.now().date() + timedelta(days=2),
        "user": {
            "username": "testuser",
            "email": "test@example.com"
        }
    }

    serializer = TaskSerializer(data=data)

    assert not serializer.is_valid()
    assert "title" in serializer.errors
