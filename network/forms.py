from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


from .models import *

class UploadPhoto(forms.ModelForm):
	class Meta:
		model = User
		fields = ('img',)


class NewPost(forms.Form):
    post = forms.CharField(widget=forms.Textarea(attrs={"rows":2, "cols":20, "class": 'form-control'}), label='')
    post.widget.attrs['placeholder'] = "What's on your mind?"