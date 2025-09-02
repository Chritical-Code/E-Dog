#Root url config

#import
#django
from django.contrib import admin
from django.urls import path, include
#images
from eDog import settings
from django.conf.urls.static import static


#url
urlpatterns = [
    path("browse/", include("browse.urls")),
    path("", include("browse.urls")),
    path("user/", include("user.urls")),
    path("post/", include("post.urls")),
    #path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


