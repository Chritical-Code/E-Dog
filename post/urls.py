#Post url config

#import
from django.urls import path
from . import views


#url
urlpatterns = [
    path("manage/", views.postManager, name="postManager"),
    path("tryCreatePost/", views.tryCreatePost, name="tryCreatePost"),
    path("edit/<int:postID>/", views.editPost, name="editPost"),
    path("fetchEditDeletePic/", views.fetchEditDeletePic, name="fetchEditDeletePic"),
    path("fetchUploadImage/", views.fetchUploadImage, name="fetchUploadImage"),
    path("fetchMaxPostsCheck/", views.fetchMaxPostsCheck, name="fetchMaxPostsCheck"),
    path("dodelete/", views.doDeletePost, name="doDeletePost"),
    path("<int:postID>/", views.index, name="index"),
]