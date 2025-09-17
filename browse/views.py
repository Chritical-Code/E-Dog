#Browse views

#import
from django.shortcuts import render, redirect
from post.models import Post, Image
from .forms import SearchForm
from post.postBox import PostBox

#views
#index
def index(request):
    #createa a form
    searchForm = SearchForm()

    #retrieve recent posts
    recentPosts = Post.objects.filter(image__isnull=False).distinct().exclude(breeds="").order_by("-dateCreated")[:10]

    #retrieve random posts
    randomPosts = Post.objects.filter(image__isnull=False).distinct().exclude(breeds="").order_by("?")[:10]

    #retrieve youngest dog posts
    youngestPosts = Post.objects.filter(image__isnull=False).distinct().exclude(breeds="").order_by("-age")[:10]

    #postboxify posts
    linkType = "/post/"
    recentPostBoxes = PostBox.easyCombine(recentPosts, linkType)
    randomPostBoxes = PostBox.easyCombine(randomPosts, linkType)
    youngestPostBoxes = PostBox.easyCombine(youngestPosts, linkType)

    #attach variables to context
    context = {
        "recentPostBoxes": recentPostBoxes,
        "randomPostBoxes": randomPostBoxes,
        "youngestPostBoxes": youngestPostBoxes,
        "searchForm": searchForm,
        "username": request.user.username,
    }
    
    #return render
    return render(request, "browse/index.html", context)



#search
def search(request, searchStr):
    #createa a form
    searchForm = SearchForm()
    
    #retrieve all posts related to search
    relatedPosts = Post.objects.filter(breeds__icontains=searchStr)[:10]
    
    #postBoxify posts
    postBoxes = PostBox.easyCombine(relatedPosts, "/post/")

    context = {
        "postBoxes": postBoxes,
        "searchStr": searchStr,
        "searchForm" : SearchForm,
    }

    return render(request, "browse/search.html", context)

    

#searchbar
def searchBar(request):
    searcho = request.POST.get("searcho")
    return redirect("/browse/search/" + searcho + "/")


#about
def about(request):
    context = {}
    return render(request, "browse/about.html", context)