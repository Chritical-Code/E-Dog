from django.contrib import admin
from .models import Post
from .models import Image

# Register your models here.
admin.site.register(Post)


#image
class imageAdmin(admin.ModelAdmin):
    list_display = ["title", "photo"]

admin.site.register(Image, imageAdmin)