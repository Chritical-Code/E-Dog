import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from post.postBox import PostBox
from post.models import Post, Image, Approved
from django.db.models import Q

@login_required
def index(request):
    #staff only
    if(request.user.is_staff != True):
        return redirect("/browse/")
    
    context = {}
    return render(request, "staff/index.html", context)

@login_required
def approval(request):
    #staff only
    if(request.user.is_staff != True):
        return redirect("/browse/")

    #retrieve recent posts
    unapprovedPosts = (
        Post.objects.filter(image__isnull=False).distinct() #has images
        .filter(approved__isnull=True).distinct() #unapproved
        .order_by("dateCreated")[:10] #oldest first, stop at 10
    )
    
    linkType = "/staff/review/"
    unapprovedPostBoxes = PostBox.easyCombine(unapprovedPosts, linkType)

    context = {
        "unapprovedPostBoxes": unapprovedPostBoxes
    }
    return render(request, "staff/approval.html", context)

@login_required
def review(request, postID):
    #staff only
    if(request.user.is_staff != True):
        return redirect("/browse/")
    
    post = get_object_or_404(Post, pk=postID)
    allImages = Image.objects.filter(post=postID)

    context = {
        "post": post,
        "allImages": allImages,
    }

    return render(request, "staff/review.html", context)

@login_required
def doApprove(request):
    #staff only, post only
    if((request.user.is_staff != True) or (request.method != "POST")):
        return redirect("/browse/")
    
    #get post
    postPK = request.POST["postPK"]
    post = Post.objects.filter(pk=postPK)[0]

    #approve post
    postApproval = Approved()
    postApproval.post = post
    postApproval.approved = True
    postApproval.save()

    return redirect("staff_approval")

@login_required
def doDelete(request):
    #staff only, post only
    if((request.user.is_staff != True) or (request.method != "POST")):
        return redirect("/browse/")
    
    #get post
    postPK = request.POST["postPK"]
    post = Post.objects.filter(pk=postPK)[0]

    #delete related images
    images = Image.objects.filter(post=post.pk)
    for image in images:
        if os.path.exists(image.photo.path):
            os.remove(image.photo.path)

    #delete
    post.delete()

    return redirect("staff_approval")