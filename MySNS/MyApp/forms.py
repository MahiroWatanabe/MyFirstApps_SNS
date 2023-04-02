from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Talk, Post

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=False, help_text='Required. Enter a valid email address.')
    github_id = forms.CharField(required=False, max_length=100)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'github_id')

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image','image2', 'image3', 'image4', 'image5', 'category']


class TalkForm(forms.ModelForm):
    class Meta:
        model = Talk
        fields = ['content']
