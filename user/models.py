#import
from django.db import models
from django.contrib.auth.models import User

#models
class Pinned(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pinnedPosts = models.JSONField()