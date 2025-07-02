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

    #retrieve recent 10 posts
    latestPosts = Post.objects.order_by("-dateCreated")[:10]

    #combine posts with their respective images
    postBoxes = []
    for post in latestPosts:
        postImages = Image.objects.filter(post=post.pk)[:1]

        if postImages:
            thumbnail = postImages[0]
        else:
            thumbnail = None

        aPost = PostBox(thumbnail, post, f"/post/{post.pk}")
        postBoxes.append(aPost)

    #attach variables to context
    context = {
        "postBoxes": postBoxes,
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
    
    #combine posts with their respective images
    postBoxes = []
    for post in relatedPosts:
        postImages = Image.objects.filter(post=post.pk)[:1]

        if postImages:
            thumbnail = postImages[0]
        else:
            thumbnail = None

        aPost = PostBox(thumbnail, post, f"/post/{post.pk}")
        postBoxes.append(aPost)

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