from django.contrib import admin
from django.urls import path, include
from eDog import settings
from django.conf.urls.static import static


urlpatterns = [
    path("browse/", include("browse.urls")),
    path("", include("browse.urls")),
    path("user/", include("user.urls")),
    path("post/", include("post.urls")),
    path("staff/", include("staff.urls")),
    #path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


