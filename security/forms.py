from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from customization_22.models import CustomUser


class RegisterForm(UserCreationForm):
    """A user registration form based on Django's built-in UserCreationForm
    """
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
