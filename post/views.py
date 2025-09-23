#import
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Image, Approved
from .forms import CreatePost, UploadImage
from django.contrib.auth.decorators import login_required
import datetime, decimal, os, random, json
from django.http import JsonResponse
from post.postBox import PostBox

#views
#index
def index(request, postID):
    post = get_object_or_404(Post, pk=postID)
    postKey = post.pk
    allImages = Image.objects.filter(post=postKey)

    context = {
        "post": post,
        "allImages": allImages,
    }

    return render(request, "post/index.html", context)

@login_required
#post Manager
def postManager(request):
    #get all of this user's posts
    posts = Post.objects.filter(user=request.user.pk)
    
    #postBoxify posts
    postBoxes = PostBox.easyCombine(posts, "/post/edit/")

    context = {
        "postBoxes": postBoxes,
    }

    return render(request, "post/postManager.html", context)

#try create post
@login_required
def tryCreatePost(request):
    #get users posts
    userPosts = Post.objects.filter(user=request.user)
    
    #cancel if user has max posts already
    if len(userPosts) >= 10:
        return redirect("postManager")
    
    #check each of user's post for a pre-existing unfinished one
    for blankPost in userPosts:
        if blankPost.breeds == "":
            return redirect("/post/edit/" + str(blankPost.pk) + "/")

    #otherwise make a blank post to edit
    post = Post()
    user = request.user
    age = datetime.date.today()
    post.user = user
    post.breeds = ""
    post.price = decimal.Decimal(0)
    post.description = ""
    post.age = age
    post.save()

    return redirect("/post/edit/" + str(post.pk) + "/")

#edit post
@login_required
def editPost(request, postID):
    if request.method == "GET":
        #get post
        post = get_object_or_404(Post, pk=postID)

        #check if wrong user
        if not(request.user.pk == post.user.pk):
            print("wrong user")
            return redirect("/browse/")

        #form
        forminitial = {
            "breeds": post.breeds,
            "price": post.price,
            "age": post.age,
            "description": post.description,
        }
        editPostForm = CreatePost(initial=forminitial)
        uploadImageForm = UploadImage()

        #get images
        allImages = Image.objects.filter(post=post.pk)
        
        context = {
            "editPostForm": editPostForm,
            "postPK": post.pk,
            "uploadImageForm": uploadImageForm,
            "allImages": allImages,
        }

        return render(request, "post/editPost.html", context)
    elif request.method == "POST":
        return doEditPost(request)

#do edit post
def doEditPost(request):
    #get post
    postPK = request.POST["postPK"]
    post = Post.objects.filter(pk=postPK)[0]

    #check if wrong user
    if not(request.user.pk == post.user.pk):
        print("wrong user")
        return redirect("/browse/")
    
    #prepare forms and images
    editPostForm = CreatePost(request.POST)
    uploadImageForm = UploadImage()
    allImages = Image.objects.filter(post=post.pk)

    #check if form has errors
    if not editPostForm.is_valid():
        context = {
            "editPostForm": editPostForm,
            "postPK": post.pk,
            "uploadImageForm": uploadImageForm,
            "allImages": allImages,
        }

        return render(request, "post/editPost.html", context)

    #get data
    breeds = editPostForm.cleaned_data["breeds"]
    price = editPostForm.cleaned_data["price"]
    description = editPostForm.cleaned_data["description"]
    age = editPostForm.cleaned_data["age"]

    #update post
    post.breeds = breeds
    post.price = price
    post.description = description
    post.age = age
    post.save()

    #unapprove post
    unApprovePost(post.pk)

    return redirect("postManager")

#do delete post
@login_required
def doDeletePost(request):
    #get post
    postPK = request.POST["postPK"]
    post = Post.objects.filter(pk=postPK)[0]

    #check if wrong user
    if not(request.user.pk == post.user.pk):
        print("wrong user")
        return redirect("/browse/")
    
    #delete related images
    images = Image.objects.filter(post=post.pk)
    for image in images:
        if os.path.exists(image.photo.path):
            os.remove(image.photo.path)

    #delete
    post.delete()


    return redirect("/post/manage")

#remove post from approval list
def unApprovePost(postPK):
    approvals = Approved.objects.filter(post=postPK)
    for approval in approvals:
        approval.delete()

#fetch
#delete's an image
def fetchEditDeletePic(request):
    #parse sent body data
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    imagePK = int(body["imagePK"])

    #delete selected picture
    images = Image.objects.filter(id=imagePK)
    for image in images:
        if os.path.exists(image.photo.path):
            os.remove(image.photo.path)
        image.delete()

    #misc
    context = {}
    return JsonResponse(context, safe=True)

#pre-process for uploading images
def fetchUploadImage(request):
    #get post
    postPK = request.POST["postPK"]
    post = Post.objects.filter(pk=postPK)[0]

    #cancel if wrong user
    if not(request.user.pk == post.user.pk):
        print("wrong user - image upload")
        return
    
    #cancel if post has too many images
    allImages = Image.objects.filter(post=post.pk)
    if len(allImages) >= 10:
        context["error"] = "This post has the maximum allowed pictures (10)."
        return JsonResponse(context, safe=True)

    #attempt upload image to server
    photoPK = funcUploadImage(request, post)

    #cancel if image upload failed
    if(photoPK == False):
        context["error"] = "Image upload failed."
        return JsonResponse(context, safe=True)

    #get image from db
    image = Image.objects.filter(pk=photoPK)[0]

    #send image to user
    context = {
        "imgUrl": image.photo.url,
        "imgPK": image.pk,
    }
    return JsonResponse(context, safe=True)

#actual image upload
def funcUploadImage(request, post):
    #create image and add data
    img = Image()
    img.title = "img_title"
    img.post = post

    #send to image form
    imgForm = UploadImage(request.POST, request.FILES, instance=img)

    #save if valid
    if imgForm.is_valid():
        imgForm.save()
        unApprovePost(post.pk)
        return img.pk
    else:
        return False
    
#check if we're maxxed out on posts
def fetchMaxPostsCheck(request):
    context = {}
    
    #cancel if too many posts
    allPosts = Post.objects.filter(user_id=request.user.pk)
    if len(allPosts) >= 10:
        context["error"] = "You have the maximum allowed posts (10)."
    
    return JsonResponse(context, safe=True)