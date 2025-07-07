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
    latestPosts = Post.objects.order_by("-dateCreated")[:10]

    #retrieve featured posts
    featuredPosts = Post.objects.order_by("-dateCreated")[:10]

    #retrieve random posts
    randomPosts = Post.objects.order_by("-dateCreated")[:10]

    #postboxify posts
    linkType = "/post/"
    latestPostBoxes = PostBox.easyCombine(latestPosts, linkType)
    featuredPostBoxes = PostBox.easyCombine(featuredPosts, linkType)
    randomPostBoxes = PostBox.easyCombine(randomPosts, linkType)

    #attach variables to context
    context = {
        "featuredPostBoxes": featuredPostBoxes,
        "randomPostBoxes": randomPostBoxes,
        "latestPostBoxes": latestPostBoxes,
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