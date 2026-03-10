from django import forms
from django.core.exceptions import ValidationError
from .models import Post
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
import re
from .models import Tag


def validate_no_bad_words(value: str) -> None:
    """Validator that raises ValidationError if text contains forbidden words
    """
    bad_words = ["spam", "hack", "fake"]

    for word in bad_words:
        if word in value.lower():
            raise ValidationError("Text contains forbidden words!")


class CategorySelectWidget(forms.Select):
    """Custom select widget with additional CSS class
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.attrs.update({
            "class": "custom-select"
        })


class PostForm(forms.ModelForm):
    """Form for creating/editing Post objects with validation
    """
    content = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 5}),
        validators=[validate_no_bad_words]
    )

    class Meta:
        model = Post
        fields = ["title", "content"]

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control"
            }),
        }

    def clean_title(self) -> str:
        """Validate title length (at least 5 characters)
        """
        title = self.cleaned_data["title"]

        if len(title) < 5:
            raise forms.ValidationError(
                "Title must be at least 5 characters"
            )

        return title


class RegisterForm(UserCreationForm):
    """User registration form with custom phone number validation
    """

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "email",
            "phone_number",
            "password1",
            "password2",
        ]

    def clean_phone_number(self) -> str:
        """Validate that phone number starts with '+'
        """
        phone = self.cleaned_data["phone_number"]

        if not phone.startswith("+"):
            raise forms.ValidationError(
                "Phone number must start with +"
            )

        return phone


class HexColorField(forms.CharField):
    """Form field that validates input as a HEX color code
    """

    def validate(self, value) -> None:
        """Validate that the value is a valid HEX color code
        """
        super().validate(value)
        if not re.fullmatch(r"#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})", value):
            raise forms.ValidationError("Enter a valid HEX color code (e.g., #FF5733).")


class ColorForm(forms.Form):
    """Form for entering a favorite HEX color
    """
    favorite_color = HexColorField(max_length=7)


class TagForm(forms.ModelForm):
    """Form for creating/editing Tag objects (UpperCaseCharField used in model)
    """

    class Meta:
        model = Tag
        fields = ["name"]
