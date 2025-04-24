#Post models

#import
from django.db import models

from django.contrib.auth.models import User



#post
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    breeds = models.CharField(max_length=200)
    price = models.DecimalField(decimal_places=2, max_digits=9)
    description = models.TextField()
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
    

#image
class Image(models.Model):
    photo = models.ImageField(upload_to="pics/%Y/%m/%d/")
    title = models.CharField(max_length=20)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)