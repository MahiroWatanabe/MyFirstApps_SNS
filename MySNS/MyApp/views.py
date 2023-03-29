from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy

from django.views.generic import ListView, CreateView, DetailView

from django.db.models import Count

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse

from django.views.decorators.http import require_POST

from .models import Post, PostLike, Talk
from .forms import CustomUserCreationForm

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
    
class PostDetailView(DetailView):
    model = Post
    template_name = 'postDetail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        postlike_count = self.object.postlike_set.count()
        # ポストに対するイイね数
        context['postlike_count'] = postlike_count
        # ログイン中のユーザーがイイねしているかどうか
        if self.object.postlike_set.filter(user=self.request.user).exists():
            context['is_user_liked_for_post'] = True
        else:
            context['is_user_liked_for_post'] = False

        return context

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

class SignupView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('MyApp:index')
    template_name = 'signup.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        # ユーザーが作成された場合はログインする
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return response
    
@require_POST
@login_required
def post_like(request):
    post_pk = request.POST.get('post_pk')
    context = {
        'user': f'{ request.user }',
    }
    post = get_object_or_404(Post, pk=post_pk)
    like = PostLike.objects.filter(post=post, user=request.user)

    if like.exists():
        like.delete()
        context['method'] = 'delete'
    else:
        like.create(post=post, user=request.user)
        context['method'] = 'create'

    context['postlike_count'] = post.postlike_set.count()

    return JsonResponse(context)

    

def login_signup(request):
    login_form = AuthenticationForm(request=request)
    signup_form = CustomUserCreationForm()
    
    if request.method == 'POST':
        if 'login_form_submit' in request.POST:
            login_form = AuthenticationForm(request=request, data=request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')
                user = authenticate(request=request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('MyApp:index')
        elif 'signup_form_submit' in request.POST:
            signup_form = UserCreationForm(request.POST)
            if signup_form.is_valid():
                signup_form.save()
                username = signup_form.cleaned_data.get('username')
                password = signup_form.cleaned_data.get('password1')
                user = authenticate(request=request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('MyApp:index')

    context = {
        'login_form': login_form,
        'signup_form': signup_form
    }
    return render(request, 'login.html', context)
