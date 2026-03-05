from django import forms
from django.utils import timezone
from .models import Task
from datetime import date


class TaskForm(forms.ModelForm):
    """Form for creating and updating Task
    """

    class Meta:
        model = Task
        fields = ["title", "description", "due_date"]

    def clean_due_date(self) -> date:
        """Validate that the due_date is not in the past
        """
        due_date = self.cleaned_data.get("due_date")

        if due_date and due_date < timezone.now().date():
            raise forms.ValidationError("Date cannot be in the past.")

        return due_date
