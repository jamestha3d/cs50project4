from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime
from django.utils import timezone

class User(AbstractUser, models.Model):
    followings = models.ManyToManyField('self', related_name="followers", symmetrical=False)
    #users = queryset
    #follower = follower created normally
    #for user in users.iterator():
        #follower.followings.add(user)
    def __str__(self):
        return f"{self.username} Posts { self.posts.all().count()} follows: {self.followings.all().count()} followers:{self.followers.all().count()} "



class Posts(models.Model):
    content = models.CharField(max_length=200)
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    likes = models.IntegerField(default=0)
    date = models.DateTimeField(default=datetime.now())
    likers = models.ManyToManyField(User, blank=True, related_name="posts_liked")
    #liked = models.BooleanField()

    #users = queryset
    #post = Post created normally
    #for user in users.iterator():
        #post.likes.add(user)


    def __str__(self):
        return f" \n Post: {self.content} by {self.poster} \n  {self.likers.all().count()} likes"

    def num_likes(self):
        return self.likers.all().count()



