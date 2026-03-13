from django import forms


class LoginForm(forms.Form):
    """Form for user login that collects user's name and age
    """
    name = forms.CharField(max_length=100)
    age = forms.IntegerField(min_value=1, max_value=120)
