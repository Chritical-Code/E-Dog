from django import forms

class SearchForm(forms.Form):
    searcho = forms.CharField(label="Search:", max_length=100)