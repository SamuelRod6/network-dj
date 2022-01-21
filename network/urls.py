
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("following/<str:username>", views.following, name="following"),

    # API Routes
    path("edit/<int:post_id>", views.edit_post, name="edit"),
    path("like/<int:post_id>", views.like_post, name="like"),
]
