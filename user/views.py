#User views
#import
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import JsonResponse

from .forms import SignupForm
from post.models import Post
from.models import Pinned
from post.postBox import PostBox


#views
def index(request, reqName):
    #retrieve all of this user's posts
    user = get_object_or_404(User, username=reqName)
    userKey = user.pk
    userPosts = Post.objects.filter(user=userKey)

    #postBoxify posts
    postBoxes = PostBox.easyCombine(userPosts, "/post/")

    context = {
        "user": user,
        "postBoxes": postBoxes,
    }

    return render(request, "user/index.html", context)

@login_required
def showAccount(request):
    context = {
        "user": request.user,
    }

    return render(request, "user/myAccount.html", context)

def loginPage(request):
    if(request.method == "GET"):
        loginForm = AuthenticationForm()

        context = {
            "loginForm": loginForm
        }

        return render(request, "user/login.html", context)
    elif request.method == "POST":
        return doLogin(request)

def doLogin(request):
    #get form
    loginForm = AuthenticationForm(request, request.POST)

    #check if valid
    if loginForm.is_valid():
        #login
        user = loginForm.get_user()
        login(request, user)
        
        #set destination
        destination = request.POST.get('next')
        if destination == "":
                destination = "/user/account/"

        return redirect(destination)
    else:
        context = {
            "loginForm": loginForm
        }
        return render(request, "user/login.html", context)

def doLogout(request):
    logout(request)
    return redirect("/user/login/")

def signUp(request):
    if request.method == "GET":
        signupForm = SignupForm()
        
        context = {
            "signupForm": signupForm,
        }
        return render(request, "user/signup.html", context)
    else:
        return doSignUp(request)

def doSignUp(request):
    signupForm = SignupForm(request.POST)

    if signupForm.is_valid():
        user = signupForm.save()
        login(request, user)
        return redirect("/user/account/")
    else:
        context = {
            "signupForm": signupForm,
        }
        return render(request, "user/signup.html", context)

@login_required
def pinned(request):
    #retrieve all of user's pinned posts
    checkPins = Pinned.objects.filter(user=request.user.pk)
    if len(checkPins) > 0:
        pinned = checkPins[0]
    #else make a pins
    else:
        userPinned = Pinned()
        userPinned.user = request.user
        userPinned.pinnedPosts = []
        userPinned.save()
        pinned = userPinned

    pinnedPosts = list()
    for post in pinned.pinnedPosts:
        filteredPosts = Post.objects.filter(pk=int(post))
        if len(filteredPosts) > 0:
            pinnedPosts.append(filteredPosts[0])
        
    #postBoxify posts
    postBoxes = PostBox.easyCombine(pinnedPosts, "/post/")

    context = {
        "postBoxes": postBoxes,
    }
    return render(request, "user/pinned.html", context)

#fetch 
# can pin, unpin, or get pin status
@login_required
def fetchTogglePin(request):
    #get data from post
    inPostPK = request.POST["postPK"]
    
    #check if we have a pins
    checkPins = Pinned.objects.filter(user=request.user.pk)
    if len(checkPins) > 0:
        userPinned = checkPins[0]
    #else make a pins
    else:
        userPinned = Pinned()
        userPinned.user = request.user
        userPinned.pinnedPosts = []
        userPinned.save()

    #if pin
    action = request.POST["action"]
    if action == "Pin":
        #check if this post is already pinned
        addPin = True
        for pin in userPinned.pinnedPosts:
            if pin == inPostPK:
                addPin = False

        #add post to pin if not duplicate
        if addPin:
            userPinned.pinnedPosts.append(inPostPK)
            userPinned.save()

        buttonToggle = "Unpin"

    #if unpin
    elif action == "Unpin":
        #remove any pins matching selected number
        for pin in userPinned.pinnedPosts:
            if pin == inPostPK:
                userPinned.pinnedPosts.remove(inPostPK)
        
        userPinned.save()
        buttonToggle = "Pin"

    #if getToggle
    else:
        #check if this post is already pinned
        hasPin = False
        for pin in userPinned.pinnedPosts:
            if pin == inPostPK:
                hasPin = True
        
        if hasPin:
            buttonToggle = "Unpin"
        else:
            buttonToggle = "Pin"

    context = {
        "count": len(userPinned.pinnedPosts),
        "buttonToggle": buttonToggle,
    }

    return JsonResponse(context, safe=True)
