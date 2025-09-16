#User url config

#import
from django.urls import path
from . import views


#url
urlpatterns = [
    path("login/", views.loginPage, name="login"),
    path("logout/", views.doLogout, name="dologout"),
    path("signup/", views.signUp, name="signup"),
    path("account/", views.showAccount, name="showAccount"),
    path("pinned/", views.pinned, name="pinned"),
    path("fetchTogglePin/", views.fetchTogglePin, name="fetchTogglePin"),
    path("<str:reqName>/", views.index, name="index"),
]