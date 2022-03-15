from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import *


class NewPost(forms.Form):
    post = forms.CharField(widget=forms.Textarea(attrs={"rows":6, "cols":30, "class": 'form-control'}))
    

def index(request):
    return render(request, "network/index.html", {"form": NewPost()})


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

def all_posts(request):
    user = request.user
    posts = Posts.objects.all().order_by("-date")
    posts_count = posts.count()
    current_page = request.GET.get('page', 1)

    paginator = Paginator(posts, 10)
    try:
        page = paginator.page(current_page)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)


    return render(request, "network/allposts.html", {
        "user": user,
        "posts": page,
        "posts_count": posts_count
        })

def following(request):
    user = request.user
    followings = user.followings.all()
    #posts = Posts.objects.filter(user in followings)
    posts_list = [user.posts.all().order_by("-date") for user in followings]
    posts = []
    for post in posts_list:
        for subset in post:
            posts.append(subset)
    posts_count= len(posts)

    current_page = request.GET.get('page', 1)

    paginator = Paginator(posts, 10)
    try:
        page = paginator.page(current_page)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

   
    return render(request, "network/following.html", {
        "posts": page,
        "followings": followings,
        "posts_count": posts_count
        })

def profile(request):
    user = request.user
    posts = user.posts.order_by("-date").all()
    posts_count = posts.count()
    num_following = user.followings.all().count() 
    num_followers = user.followers.all().count()
    current_page = request.GET.get('page', 1)
    paginator = Paginator(posts, 10)
    try:
        page = paginator.page(current_page)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return render(request, "network/profile.html", {
        "posts": page,
        "user": user,
        "num_followers": num_followers,
        "num_following": num_following,
        "posts_count": posts_count
        })


def user(request, username):
    #do something
    #loggedin = request.user
    user = request.user
    current_page = request.GET.get('page', 1)
    owner = User.objects.filter(username=username)[0]
    posts = owner.posts.order_by("-date").all()
    posts_count = posts.count()
    num_following = owner.followings.all().count() 
    num_followers = owner.followers.all().count() 
    following = user in owner.followers.all()

    paginator = Paginator(posts, 10)
    try:
        page = paginator.page(current_page)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

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
        content = request.POST["post"]
        user = request.user
        create_post = Posts(content=content, poster=user)
        create_post.save()
        #newpost = Posts.objects.create_posts(content=content, poster=user)
        #try: 
            #create_post.save()
        #except Exception as e:
            #return HttpResponse("Something went wrong!")
        return HttpResponseRedirect(reverse("profile"))
    else:
        return HttpResponseRedirect(reverse("all_posts"))


def edit(request, post_id):

    if request.method == "POST": 
        content = request.POST["post"]
        user = request.user
        post = Posts.objects.get(pk=post_id)
        post.content = content
        #post.date = datetime.now()
        post.save()
        
        return HttpResponseRedirect(reverse("profile"))
    else:
        content = Posts.objects.get(pk=post_id).content
        return render(request, "network/edit.html", {
            "form": NewPost(initial={"post" : content}),
            "post_id": post_id
            })

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
            

    return HttpResponseRedirect(reverse("user", kwargs= {"username": username}))

def like(request, post_id):

    loggedin = User.objects.filter(id = request.user.id)[0]
    post = Posts.objects.filter(id = post_id)[0]
    
    #logged in user already liked this post
    if loggedin in post.likers.all():
        #unfollow by removing loggedin user from followers
        post.likers.remove(loggedin)
        post.likes -= 1
        post.save()
    #logged in user not following    
    else:
        #add loggedin user to the followers
        post.likers.add(loggedin)
        post.likes += 1
        post.save()
    return HttpResponseRedirect(reverse("all_posts"))


def feed(request, post_id, content):
    post = Posts.objects.get(pk=post_id)
    post.content = content
    #ensure that editor is the post owner
    if request.user.id == post.poster.id:
        #post.date = datetime.now()
        post.save()
        data = {
        "status": 201
        }
        #return JsonResponse(data)
        return HttpResponse(status=200)
    else:
        return HttpResponse("You cannot edit this post!")

def like2(request, post_id):
    post = Posts.objects.get(pk=post_id)
    user = request.user
    if user in post.likers.all():
        #unfollow by removing loggedin user from followers
        post.likers.remove(user)
        post.likes -= 1
        post.save()
    #logged in user not following    
    else:
        #add loggedin user to the followers
        post.likers.add(user)
        post.likes += 1
        post.save()
    return HttpResponse(status=200)


    #update html

    