#Browse url config

#import
from django.urls import path
from . import views


#url
urlpatterns = [
    path("", views.index, name="index"),
    path("search/<str:searchStr>/", views.search, name="search"),
    path("searchbar/", views.searchBar, name="searchBar"),
    path("about/", views.about, name="about"),
]