#User views
#import
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse

from .forms import LoginForm, SignupForm
from post.models import Post, Image
from.models import Pinned
from post.postBox import PostBox


#views
#index
def index(request, reqName):
    #retrieve all of this user's posts
    user = get_object_or_404(User, username=reqName)
    userKey = user.pk
    userPosts = Post.objects.filter(user=userKey)

    #combine posts with their respective images
    postBoxes = []
    for post in userPosts:
        postImages = Image.objects.filter(post=post.pk)[:1]

        if postImages:
            thumbnail = postImages[0]
        else:
            thumbnail = None

        aPost = PostBox(thumbnail, post, f"/post/{post.pk}")
        postBoxes.append(aPost)

    context = {
        "user": user,
        "postBoxes": postBoxes,
    }

    return render(request, "user/index.html", context)

#show account
@login_required
def showAccount(request):
    context = {
        "user": request.user,
    }

    return render(request, "user/myAccount.html", context)

#login
def loginPage(request):
    loginForm = LoginForm()

    context = {
        "loginForm": loginForm
    }

    return render(request, "user/login.html", context)

#do Login
def doLogin(request):
    username = request.POST["username"]
    password = request.POST["password"]
    destination = request.POST.get('next')

    #fix destination if its empty
    if(destination == ""):
        destination = "/user/account/"

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        # Redirect to a success page.
        return redirect(destination)

    else:
        # Return an 'invalid login' error message
        return redirect(destination)
    
#do Logout
def doLogout(request):
    logout(request)
    # Redirect to a success page.
    return redirect("/user/login/")

#sign up
def signUp(request):
    signupForm = SignupForm()
    
    context = {
        "signupForm": signupForm,
    }
    return render(request, "user/signup.html", context)

#do signup
def doSignUp(request):
    #Get data from form
    username = request.POST["username"]
    password = request.POST["password"]
    email = request.POST["email"]
    firstname = request.POST["firstname"]
    lastname = request.POST["lastname"]

    #verify user name and email are available
    makeAccount = False
    if(not User.objects.filter(username=username)):
        if(not User.objects.filter(email=email)):
            makeAccount = True

    #if allowed, make the account and sign in
    if(makeAccount):
        user = User.objects.create_user(username, email, password)
        user.first_name = firstname
        user.last_name = lastname
        user.save()

        userLogin = authenticate(request, username=username, password=password)
        if userLogin is not None:
            login(request, userLogin)
    
    #redirect to account page
    return redirect("/user/account/")

#pinned posts
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
        if len(Post.objects.filter(pk=int(post))) > 0:
            pinnedPosts.append(Post.objects.filter(pk=int(post))[0])
        

    #combine posts with their respective images
    postBoxes = []
    for post in pinnedPosts:
        postImages = Image.objects.filter(post=post.pk)[:1]

        if postImages:
            thumbnail = postImages[0]
        else:
            thumbnail = None

        aPost = PostBox(thumbnail, post, f"/post/{post.pk}")
        postBoxes.append(aPost)

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
