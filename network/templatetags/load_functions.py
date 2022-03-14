from django import template
from network.models import *

register = template.Library()


def cut(value, arg):
    """Removes all values of arg from the given string"""
    return value.replace(arg, '')

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
def pages(paginator):
	pass

@register.filter
def next_page():
	pass



	

#{% load %} 
#{{ var|foo:"arg" }}