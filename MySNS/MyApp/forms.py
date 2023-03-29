from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=False, help_text='Required. Enter a valid email address.')
    github_id = forms.CharField(required=False, max_length=100)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'github_id')