import pytest
from django.utils import timezone
from datetime import timedelta
from testing.forms import TaskForm


@pytest.mark.django_db
def test_task_form_valid_data() -> None:
    """Test that form is valid when correct data is provided
    """
    data = {
        "title": "Test task",
        "description": "Test description",
        "due_date": timezone.now().date() + timedelta(days=2),
    }

    form = TaskForm(data=data)

    assert form.is_valid(), form.errors


@pytest.mark.django_db
def test_task_form_empty_required_fields() -> None:
    """Test that form fails when required fields are empty
    """
    data = {}

    form = TaskForm(data=data)

    assert not form.is_valid()
    assert "title" in form.errors
    assert "due_date" in form.errors


@pytest.mark.django_db
def test_task_form_due_date_in_past() -> None:
    """Test that form rejects due_date in the past
    """
    data = {
        "title": "Test task",
        "description": "Test description",
        "due_date": timezone.now().date() - timedelta(days=1),
    }

    form = TaskForm(data=data)

    assert not form.is_valid()
    assert "due_date" in form.errors
