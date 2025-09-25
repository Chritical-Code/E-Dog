#import
import datetime
import os
from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


#post
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    breeds = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=9)
    description = models.TextField(max_length=1000)
    age = models.DateField()
    dateCreated = models.DateField(auto_now_add=True)

    #functions
    #str (readable descriptor)
    def __str__(self):
        return f"{self.pk} {self.breeds}"
    
    #mixed?
    def checkIfMixed(self):
        #if has comma, true
        for f in self.breeds:
            if f == ',':
                return True
            
        #else false
        return False

#approved
class Approved(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    approved = models.BooleanField()

#image related
#validate image size
def validate_image_size(image):
    if image.size > 8 * 1024 * 1024:
        raise ValidationError("Image file too large (8mb)")

#generate a random file name
def custom_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    date_path = datetime.date.today().strftime('%Y/%m/%d')
    new_filename = f"{uuid4().hex}.{ext}"
    return os.path.join('pics', date_path, new_filename)

class Image(models.Model):
    photo = models.ImageField(upload_to=custom_upload_to, validators=[validate_image_size])
    title = models.CharField(max_length=20)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)