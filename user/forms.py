#user forms
#import
from django import forms

#login form
class LoginForm(forms.Form):
    username = forms.CharField(label="Username:", max_length=100)
    password = forms.CharField(label="Password:", max_length=100, widget=forms.PasswordInput)


#sign up form
class SignupForm(forms.Form):
    username = forms.CharField(label="Username:", max_length=100)
    password = forms.CharField(label="Password:", max_length=100, widget=forms.PasswordInput)
    email = forms.EmailField(label="Email:", max_length=100, widget=forms.EmailInput)

    firstname = forms.CharField(label="First Name:", max_length=100)
    lastname = forms.CharField(label="Last Name:", max_length=100)