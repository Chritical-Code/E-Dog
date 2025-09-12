#user forms
#import
from django import forms

#sign up form
class SignupForm(forms.Form):
    username = forms.CharField(label="Username:", max_length=30)
    password = forms.CharField(label="Password:", max_length=50, widget=forms.PasswordInput)
    email = forms.EmailField(label="Email:", max_length=50, widget=forms.EmailInput)

    firstname = forms.CharField(label="First Name:", max_length=30)
    lastname = forms.CharField(label="Last Name:", max_length=30)