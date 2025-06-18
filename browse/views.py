#Browse views

#import
from django.shortcuts import render, redirect
from post.models import Post, Image
from .forms import SearchForm

#views
#index
def index(request):
    #createa a form
    form = SearchForm()

    #retrieve recent 4 posts
    latestPosts = Post.objects.order_by("-dateCreated")[:10]

    #create a class to combine posts and images
    class PostAndImage:
        def __init__(self, inPost, inImage):
            self.post = inPost
            self.image = inImage

    #combine posts with their respective images         #Process:
    fullPosts = []                                      #declare empty list
    for post in latestPosts:                            #for each post:
        allImages = Image.objects.filter(post=post.pk)  #get all images
        
        if allImages:                                   #use first image, if exists
            image = allImages[0]
        else:
            image = None

        aPost = PostAndImage(post, image)               #create a temporary post object
        fullPosts.append(aPost)                         #append post object to list

    #attach variables to context
    context = {
        "fullPosts": fullPosts,
        "form": form,
        "username": request.user.username,
    }
    
    #return render
    return render(request, "browse/index.html", context)



#search
def search(request, searchStr):
    #createa a form
    form = SearchForm()
    
    #retrieve all posts related to search
    relatedPosts = Post.objects.filter(breeds__icontains=searchStr)[:10]
    
    #create a class to combine posts and images
    class PostAndImage:
        def __init__(self, inPost, inImage):
            self.post = inPost
            self.image = inImage
    
    #combine posts with their respective images         #Process:
    fullPosts = []                                      #declare empty list
    for post in relatedPosts:                           #for each post:
        allImages = Image.objects.filter(post=post.pk)  #get all images
        
        if allImages:                                   #use first image, if exists
            image = allImages[0]
        else:
            image = None

        aPost = PostAndImage(post, image)               #create a temporary post object
        fullPosts.append(aPost)                         #append post object to list

    context = {
        "fullPosts": fullPosts,
        "searchStr": searchStr,
        "form" : form,
    }

    return render(request, "browse/search.html", context)

    

#searchbar
def searchBar(request):
    searcho = request.POST.get("searcho")
    return redirect("/browse/search/" + searcho)