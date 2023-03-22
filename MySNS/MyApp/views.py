from django.shortcuts import render

from django.views.generic import ListView
from .models import Post

class UserPostListView(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        author_id = self.kwargs.get('author_id')
        # return Post.objects.filter(author_id=author_id)
        return Post.objects.filter()

