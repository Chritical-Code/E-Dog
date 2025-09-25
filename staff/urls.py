from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="staff_home"),
    path("approval/", views.approval, name="staff_approval"),
    path("doapprove/", views.doApprove, name="staff_doapprove"),
    path("dodelete/", views.doDelete, name="staff_dodelete"),
    path("review/<int:postID>/", views.review, name="staff_review"),
]