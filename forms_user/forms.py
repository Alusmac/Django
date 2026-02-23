from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


class RegistrationForm(forms.ModelForm):
    """Form for registering a new user
    """
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self) -> dict:
        """Validate that password and password_confirm match
        """
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

    def save(self, commit=True) -> User:
        """Save user with hashed password
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()

        return user


class UserProfileForm(forms.ModelForm):
    """
    Form for editing user profile + (Form Bootstrap)
    """

    bio = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control", "rows": 3}), required=False)

    birth_date = forms.DateField(widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
                                 required=False)

    location = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), required=False)

    avatar = forms.ImageField(widget=forms.ClearableFileInput(attrs={"class": "form-control"}), required=False)

    class Meta:
        model = UserProfile
        fields = ['bio', 'birth_date', 'location', 'avatar']

    def clean_avatar(self):
        """
        Validate avatar file size (max 2MB)
        """
        avatar = self.cleaned_data.get("avatar")

        if avatar and avatar.size > 2 * 1024 * 1024:
            raise forms.ValidationError(
                "Maximum file size of 2 MB"
            )

        return avatar


class CustomPasswordChangeForm(forms.Form):
    """Form for changing user password
    """
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
    confirm_new_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))

    def __init__(self, user, *args, **kwargs) -> None:
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_old_password(self) -> str:
        """Validate that old password is correct
        """
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError("Dont wright password")
        return old_password

    def clean(self) -> dict:
        """Validate that password Must differ from old password
        """
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_new_password = cleaned_data.get('confirm_new_password')
        old_password = cleaned_data.get('old_password')

        if new_password != confirm_new_password:
            raise forms.ValidationError("New passwords do not match")

        if old_password and new_password and old_password == new_password:
            raise forms.ValidationError("New passwords do not difference of each other.")

        return cleaned_data
