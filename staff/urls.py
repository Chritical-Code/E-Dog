from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("approval/", views.approval, name="approval"),
    path("review/<int:postID>/", views.review, name="review"),
]