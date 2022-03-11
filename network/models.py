from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

class User(AbstractUser, models.Model):
	"""#username
	#email
	#password
	posts = models.ForeignKey
	likes = models.ForeignKey
	followers = models.IntegerField()
	"""
	#first = models.CharField()
	#last = models.CharField()

	def __str__(self):
		return f"ID: {self.id}, username:{self.username}, email:{self.email}"

class User_info(models.Model):
	following = models.ManyToManyField(User, blank=True, related_name="likes")

	pass

class Posts(models.Model):
	content = models.CharField(max_length = 64)
	poster = models.OneToManyField(User, blank=False, related_name="poster")
	number_likes = models.IntegerField()
	#liked = models.ForeignKey.oneToMany(User, on_delete=models.CASCADE, related_name="poster" )
	date = models.DateTimeField(default=datetime.now, blank=False)
	#one post can be liked by many people. so this liked field, will probably be populated by many users. 
	#this should be extracted from this table to somwhere else


	def __str__(self):
		return f"content:{self.content} posted by {self.user} on {self.date} has {self.number_likes} likes"

class Likes(models.Model):
	"""contain post id, contain user id
	this will be another join table.
	in the forwards direction, each post with its unique id, will be related to several likers.
	this table will have a many to many relationship
	related name will be 'liked'
	each post can get its number of likers by post.likers.all()
	and each user can get all the posts he liked by user.liked.all()
	"""
	#likers = models.ManyToManyField(User, blank=True, related_name="likes")
	#liked_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likers")

	def __str__(self):
		return f" post ID: {self.posts_liked} was liked by user ID {self.liked_by}"

class Follows(models.Model):
	"""contain user id, contain other user id_
	this will be a join table that relates the relationship of following.
	user1 follows user2. 
	user1 follows user3
	user1 follows user4
	the related name will be followers.
	from user2 if we check followers, it will give us user 1
	"""

	followings = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
	followed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followings")