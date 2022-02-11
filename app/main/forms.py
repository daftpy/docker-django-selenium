from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    """
    We extend the UserCreationForm to capture the email so we are able to
    reset it for the user in the future if they forget it.
    """
    email = forms.EmailField(
        max_length=254, help_text='Required. Inform a valid email address.'
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
