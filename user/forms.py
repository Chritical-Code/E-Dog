from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import User

#sign up form
class SignupForm(UserCreationForm):
    #fields i chose to use
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
        label="Confirm Password",
        widget=forms.PasswordInput,
        max_length=50,
        help_text="",
    )

    email = forms.EmailField(
        label="Email:",
        widget=forms.EmailInput,
        max_length=50, 
    )

    first_name = forms.CharField(
        label="First Name:",
        max_length=30,
    )

    last_name = forms.CharField(
        label="Last Name:",
        max_length=30,
    )

    #which part of the model we use
    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email", "first_name", "last_name")
        field_classes = {"username": UsernameField}

    #extended saving for email and names
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user