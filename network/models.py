from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser, models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    #image = models.ImageField(default="", upload_to="profile_pics")


class post(models.Model):
    #models
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    content = models.TextField(blank=False)
    date = models.DateTimeField(default=datetime.now())
    liked = models.ManyToManyField('User', default=None, blank=True, related_name='post_likes')

    def __str__(self):
        return f" Post {self.id} made by {self.user} on {self.date.strftime('%d %b %Y %H:%M:%S')}"

