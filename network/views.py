import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Post


def index(request):
    posts = Post.objects.all().order_by('-date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'POST':
        content = request.POST["new_post"]
        new_post = Post(content=content, creator=request.user)
        new_post.save()
        return HttpResponseRedirect(reverse('index'))
    
    return render(request, 'network/index.html', {
        'posts': page_obj,
        'posts_data': reversed([post.data(request.user) for post in posts])
    })


def profile(request, username):
    profile = User.objects.get(username=username)
    posts = Post.objects.filter(creator=profile.id).order_by('-date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'POST':
        switch = request.POST.get("follow-button")
        if switch == "Follow":
            profile.followers.add(request.user)
        else:
            profile.followers.remove(request.user)
    
    return render(request, "network/profile.html", {
        "username": username,
        "posts": page_obj,
        "posts_count": posts.count(),
        "followers": profile.followers.all(),
        "followers_count": profile.followers.count(),
        "following": profile.following.count()
    })


@login_required(login_url="login")
def following(request, username):
    following = User.objects.get(username=username).following.all()
    posts = []
    for user in following:
        posts += Post.objects.filter(creator=user).all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "network/following.html", {
        "posts": page_obj
    })


@csrf_exempt
@login_required(login_url="login")
def edit_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST' and request.user == post.creator:
        new_content = json.loads(request.body).get("content").strip()
        if new_content == '':
            return JsonResponse({'error': "Post cannot be empty"}, status=400)
        post.content = new_content
        post.save()
    else:
        return JsonResponse({'error': "Request has to be POST"}, status=400)
    
    return JsonResponse({'message': "Post edited successfully"}, status=201)


@csrf_exempt
@login_required(login_url="login")
def like_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        like = json.loads(request.body).get("like")
        if like:
            post.liked_by.add(request.user)
            post.save()
        else:
            post.liked_by.remove(request.user)
            post.save()
        return HttpResponse(status=201)

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
