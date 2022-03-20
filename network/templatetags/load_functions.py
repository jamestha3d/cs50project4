from django import template
from network.models import *

register = template.Library()


#postlikes
@register.filter
def num_likes(postid):
	post = Posts.objects.filter(id=postid)[0]
	return post.num_likes()

@register.filter
def likers(postid):
	post = Posts.objects.filter(id=postid)[0]
	return post.likers.all()
	

@register.filter
def following(user_id):
	user = User.objects.get(pk=user_id)
	following_list = user.followings.all()
	return following_list
	

@register.filter
def followers(user_id):
	user = User.objects.get(pk=user_id)
	followers_list = user.followers.all()
	return followers_list
	



	

#{% load %} 
#{{ var|foo:"arg" }}