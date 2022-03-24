from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime
from django.utils import timezone
import math

class User(AbstractUser, models.Model):
    followings = models.ManyToManyField('self', related_name="followers", symmetrical=False)

    def __str__(self):
        return f"{self.username} Posts { self.posts.all().count()} follows: {self.followings.all().count()} followers:{self.followers.all().count()} "


class Posts(models.Model):
    content = models.CharField(max_length=200)
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    likes = models.IntegerField(default=0)
    date = models.DateTimeField(default=timezone.now())
    likers = models.ManyToManyField(User, blank=True, related_name="posts_liked")

    def __str__(self):
        return f" \n Post: {self.content} by {self.poster} \n  {self.likers.all().count()} likes"

    def num_likes(self):
        return self.likers.all().count()

    def time(self):
        now = timezone.now()
        
        diff= now - self.date

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            
            if seconds == 1:
                return str(seconds) +  "second ago"
            
            else:
                return str(seconds) + " seconds ago"

            

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " minute ago"
            
            else:
                return str(minutes) + " minutes ago"



        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
        
            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            

            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"


        if diff.days >= 365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"


class Comment(models.Model):
    post = models.ForeignKey(Posts,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)

