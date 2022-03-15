
from django.urls import path

from . import views

#app_name = "network"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("all_posts", views.all_posts, name="all_posts"),
    path("following", views.following, name="following"),
    path("profile", views.profile, name="profile"),
    path("user/<str:username>", views.user, name="user"),
    path("create", views.make_post, name="make_post"),
    path("follow/<str:user_id>", views.follow, name="follow"),
    path("like/<str:post_id>", views.like, name="like"),
    path("edit/<str:post_id>", views.edit, name="edit"),
    path("feed/<int:post_id>/<str:content>", views.feed, name="feed"),
    path("like2/<int:post_id>", views.like2, name="like2")
]
