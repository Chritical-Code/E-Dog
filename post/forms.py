#post forms
#import
from django import forms
from .models import Image
import datetime


#forms
#Create Post
class CreatePost(forms.Form):
    #create a list of valid years for use with age
    currentYear = datetime.date.today().year
    validYears = []
    x = 40
    while x > -1:
        validYears.append(currentYear - x)
        x -= 1    
    validYears.sort(reverse=True)

    #form entries
    breeds = forms.CharField(label="Breeds:", max_length=100)
    price = forms.DecimalField(label="Price:", decimal_places=2, max_digits=9)
    age = forms.DateField(label="Date Born:", widget=forms.SelectDateWidget(years=validYears))
    description = forms.CharField(label="Description:", max_length=100, widget=forms.Textarea)


#Upload Image
class UploadImage(forms.ModelForm):
    class Meta:
        model = Image
        exclude = ["title", "post"]

