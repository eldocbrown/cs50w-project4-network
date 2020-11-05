from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Post
from .forms import PostForm


def index(request):
    # TODO: Pagination
    posts = Post.objects.all().order_by('-created_at')
    return render(request, "network/index.html", {
        "posts": posts,
        "postForm": PostForm()
    });

def profile(request, usernamestr):
    if request.method == "POST":
        raise Http404("Only GET requests allowed on this URL")

    try:
        u = User.objects.get(username=usernamestr)
        followingCount = u.following.count()
        followersCount = u.followers.all().count()
        userPosts = u.usrPosts.all().order_by("-created_at")
    except Exception as e:
        raise Http404(f"Error while retrieving user data from {usernamestr}")

    return render(request, "network/profile.html", {
        "followingCount": followingCount,
        "followersCount": followersCount,
        "userPosts": userPosts,
        "usernamestr": usernamestr
    });

@login_required(login_url="network:login")
def post(request):
    if request.method == "POST":
        f = PostForm(request.POST)
        if f.is_valid():
            newPost = f.save(commit=False)
            newPost.user = request.user
            newPost.save()
            f.save_m2m()
            return HttpResponseRedirect(reverse("network:index"))
        else:
            # TODO: Render error message
            return render(request, "network/index.html", {
                "postForm": PostForm()
            });
    else:
        raise Http404("Only POST request allowed on this URL")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("network:index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("network:index"))


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
        return HttpResponseRedirect(reverse("network:index"))
    else:
        return render(request, "network/register.html")
