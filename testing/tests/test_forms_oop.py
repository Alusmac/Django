from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from testing.forms import TaskForm


class TaskFormTest(TestCase):
    """Test suite for TaskForm validation
    """

    def test_form_valid_data(self) -> None:
        """Test that form is valid when correct data is provided
        """
        form_data = {
            "title": "Test task",
            "description": "Test description",
            "due_date": timezone.now().date() + timedelta(days=1),
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_empty_required_fields(self) -> None:
        """Test that form fails when required fields are empty
        """
        form = TaskForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)
        self.assertIn("due_date", form.errors)

    def test_due_date_cannot_be_in_past(self) -> None:
        """Test that form rejects due_date in the past
        """
        form_data = {
            "title": "Test task",
            "description": "Test description",
            "due_date": timezone.now().date() - timedelta(days=1),
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("due_date", form.errors)
