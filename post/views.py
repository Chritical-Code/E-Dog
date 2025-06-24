#Post views
#import
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Image
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

    #combine posts with their respective images
    postBoxes = []
    for post in posts:
        postImages = Image.objects.filter(post=post.pk)[:1]

        if postImages:
            thumbnail = postImages[0]
        else:
            thumbnail = None

        aPost = PostBox(thumbnail, post, f"/post/edit/{post.pk}")
        postBoxes.append(aPost)

    context = {
        "postBoxes": postBoxes,
    }

    return render(request, "post/postManager.html", context)

#try create post
@login_required
def tryCreatePost(request):
    #first check each of user's post for a pre-existing blank one
    userPosts = Post.objects.filter(user=request.user)
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

#do edit post
@login_required
def doEditPost(request):
    #get post
    postPK = request.POST["postPK"]
    post = Post.objects.filter(pk=postPK)[0]

    #check if wrong user
    if not(request.user.pk == post.user.pk):
        print("wrong user")
        return redirect("/browse/")

    #get data
    breeds = request.POST["breeds"]
    price = request.POST["price"]
    description = request.POST["description"]
    #create datetime from input
    year = int(request.POST["age_year"])
    month = int(request.POST["age_month"])
    day = int(request.POST["age_day"])
    age = datetime.date(year=year, month=month, day=day)

    #update post
    post.breeds = breeds
    post.price = price
    post.description = description
    post.age = age
    post.save()

    return redirect("/post/manage/")

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

#fetch
#edit post delete image
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

#upload image
def fetchUploadImage(request):
    #tofix: maybe check if login is right or is right account?

    #get post
    postPK = request.POST["postPK"]
    post = Post.objects.filter(pk=postPK)[0]

    #upload image to server
    photoPK = funcUploadImage(request, post)

    #get image we just uploaded
    image = False
    if(photoPK):
        image = Image.objects.filter(pk=photoPK)[0]

    #misc
    context = {
        "imgUrl": image.photo.url,
        "imgPK": image.pk,
    }
    return JsonResponse(context, safe=True)

#function upload image
def funcUploadImage(request, post):
    #create image and add data
    img = Image()
    img.title = "img_title"
    img.post = post
    imgForm = UploadImage(request.POST, request.FILES, instance=img)
    if imgForm.is_valid():
        imgForm.save()
        return img.pk
    else:
        return False