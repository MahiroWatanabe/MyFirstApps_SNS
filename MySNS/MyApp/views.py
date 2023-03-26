from django.shortcuts import get_object_or_404, render

from django.views.generic import ListView, CreateView
from .models import Post, PostLike, Talk
from django.db.models import Count

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

class UserPostListView(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        author_id = self.kwargs.get('author_id')
        # return Post.objects.filter(author_id=author_id)
        return Post.objects.filter()

class TalkView(ListView):
    model = Talk
    template_name = 'talk.html'
    context_object_name = 'talks'
    
    # def get_queryset(self):
    #     author_id = self.kwargs.get('author_id')
    #     # return Post.objects.filter(author_id=author_id)
    #     return Post.objects.filter()

class TalkDetailView(ListView):
    model = Talk
    template_name = 'talk.html'
    context_object_name = 'talks'

class TalkCreateView(CreateView):
    model = Talk
    template_name = 'talk.html'
    context_object_name = 'talks'

class PostView(ListView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if 'popularity' in self.request.GET:
            queryset = queryset.annotate(num_likes=Count('postlike')).order_by('-num_likes')
        else:
            queryset = queryset.order_by('-date_posted')
        return queryset
    
class PostDetailView(ListView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

class PostCreateView(CreateView):
    model = Post
    template_name = 'post.html'
    # context_object_name = 'posts'
    
    # def get_queryset(self):
    #     author_id = self.kwargs.get('author_id')
    #     # return Post.objects.filter(author_id=author_id)
    #     return Post.objects.filter()

class MyPageView(ListView):
    model = Post
    template_name = 'myPage.html'
    # context_object_name = 'posts'
    
    # def get_queryset(self):
    #     author_id = self.kwargs.get('author_id')
    #     # return Post.objects.filter(author_id=author_id)
    #     return Post.objects.filter()

@require_POST
@login_required
def post_like(request):
    post_id = request.POST.get('post_id')
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    liked = False
    if post.likes.filter(id=user.id).exists():
        post.likes.remove(user)
    else:
        post.likes.add(user)
        liked = True
    context = {
        'liked': liked,
        'count': post.likes.count()
    }
    return JsonResponse(context)