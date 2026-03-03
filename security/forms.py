from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class RegisterForm(UserCreationForm):
    """A user registration form based on Django's built-in UserCreationForm
    """
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
