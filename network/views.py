from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from django.urls import reverse
from django import forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import *
from .forms import UploadPhoto, NewPost
    

def index(request):
    user = request.user
    if user.is_authenticated:
        posts = Posts.objects.all().order_by("-id")
        posts_count = posts.count()
        current_page = request.GET.get('page', 1)
        page = paginate(posts, current_page)
        return render(request, "network/index.html", {
            "form": NewPost(),
            "user": user,
            "posts": page,
            "posts_count": posts_count
            })
    else:
        return HttpResponseRedirect(reverse("login"))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def image_upload_view(request):
    """Process images uploaded by users"""
    if request.method == 'POST':
        #image is in request.files
        user= request.user
        form = UploadPhoto(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("profile"))
        else:
            form = UploadPhoto()
            return render(request, 'profile.html', {
                'form': form
            })

def all_posts(request):
    user = request.user
    if user.is_authenticated:
        posts = Posts.objects.all().order_by("-id")
        posts_count = posts.count()
        current_page = request.GET.get('page', 1)
        page = paginate(posts, current_page)
        return render(request, "network/allposts.html", {
            "user": user,
            "posts": page,
            "posts_count": posts_count
            })
    else:
        return HttpResponseRedirect(reverse("login"))

def following(request):
    user = request.user
    #select posts where user in followings of current user
    posts = Posts.objects.filter(poster__in=user.followings.all()).order_by("-id")
    posts_count= len(posts)
    current_page = request.GET.get('page', 1)
    page = paginate(posts, current_page)

   
    return render(request, "network/following.html", {
        "posts": page,
        "posts_count": posts_count
        })

def profile(request):
    user = request.user
    posts = user.posts.all().order_by("-id")
    posts_count = posts.count()
    num_following = user.followings.all().count() 
    num_followers = user.followers.all().count()
    current_page = request.GET.get('page', 1)
    page = paginate(posts, current_page)
    form = UploadPhoto()

    return render(request, "network/profile.html", {
        "posts": page,
        "user": user,
        "num_followers": num_followers,
        "num_following": num_following,
        "posts_count": posts_count,
        "form": form
        })


def user(request, username):
    user = request.user
    current_page = request.GET.get('page', 1)
    owner = User.objects.filter(username=username)[0]
    posts = owner.posts.all().order_by("-id")
    posts_count = posts.count()
    num_following = owner.followings.all().count() 
    num_followers = owner.followers.all().count() 
    following = user in owner.followers.all()
    page = paginate(posts, current_page)

    return render(request, "network/user.html", {
        "posts": page,
        "user2": owner,
        "num_followers": num_followers,
        "num_following": num_following,
        "following": following,
        "posts_count": posts_count
        })

def make_post(request):
    if request.method == "POST": 
        content = request.POST["post"].strip().capitalize()
        user = request.user
        create_post = Posts(content=content, poster=user)
        create_post.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseRedirect(reverse("index"))

def comment(request, post_id, comment):
    content = comment.strip().capitalize()
    post = Posts.objects.get(pk=post_id)
    user = request.user
    create_comment = Comment(post= post, poster=user, content=content)
    create_comment.save()
    data = {
        "status": 200,
        "commented": True,
    }

    return JsonResponse(data)

def follow(request, user_id):

    loggedin = User.objects.filter(id = request.user.id)[0]
    tofollow = User.objects.filter(id = user_id)[0]
    username = tofollow.username
    #logged in user already following this person
    if loggedin in tofollow.followers.all():
        #unfollow by removing loggedin user from followers
        tofollow.followers.remove(loggedin)
    #logged in user not following    
    else:
        #add loggedin user to the followers
        tofollow.followers.add(loggedin)

    data = {
    "status": 200,
    "follow": True,
    }

    return JsonResponse(data)


def edit(request, post_id, content):
    post = Posts.objects.get(pk=post_id)
    post.content = content.strip().capitalize()
    #ensure that editor is the post owner
    if request.user.id == post.poster.id:
        post.save()
        data = {
        "status": 200
        }
        return JsonResponse(data)
    else:
        return HttpResponse("You cannot edit this post!")

def like(request, post_id):
    post = Posts.objects.get(pk=post_id)
    user = request.user
    if user in post.likers.all():
        #unlike by removing loggedin user from likers
        post.likers.remove(user)
        post.likes -= 1
        post.save()  
        data = {
        "status": 200,
        "like": True,
        } 
    else:
        #add user to likers
        post.likers.add(user)
        post.likes += 1
        post.save()
        data = {
        "status": 200,
        "unlike": True,
        }
    return JsonResponse(data)

def delete(request,post_id):

    post = Posts.objects.get(pk=post_id)
    user = request.user
    if request.user.id == post.poster.id:
        #delete posts
        post.delete()
        data = {
        "status": 200,
        "delete": True,
        }
        return JsonResponse(data)
    else:
        return HttpResponse('You do have the authority to delete this post!')



def paginate(posts, current_page):

    paginator = Paginator(posts, 10)
    try:
        page = paginator.page(current_page)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return page







    