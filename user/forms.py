#user forms
#import
from django import forms
from django.contrib.auth.forms import UserCreationForm

#sign up form
class SignupForm(UserCreationForm):
    username = forms.CharField(
        label="Username:",
        max_length=30,
        help_text="",
    )

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        help_text="",
        max_length=50,
    )

    password2 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        max_length=50,
        help_text="",
    )

    email = forms.EmailField(
        label="Email:",
        widget=forms.EmailInput,
        max_length=50, 
    )

    firstname = forms.CharField(
        label="First Name:",
        max_length=30,
    )

    lastname = forms.CharField(
        label="Last Name:",
        max_length=30,
    )