from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy

from django.views.generic import ListView, CreateView, DetailView, UpdateView, TemplateView

from django.db.models import Count

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import JsonResponse

from django.views.decorators.http import require_POST

from .models import Post, PostLike, Talk, TalkLike, Profile

from .forms import CustomUserCreationForm, TalkForm, PostForm

class UserPostListView(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        author_id = self.kwargs.get('author_id')
        # return Post.objects.filter(author_id=author_id)
        return Post.objects.filter()

#------Post-----

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        postlike_counts = []
        is_user_liked_for_posts = []
        for post in context['posts']:
            postlike_count = post.postlike_set.count()
            postlike_counts.append(postlike_count)
            
            if post.postlike_set.filter(user=self.request.user).exists():
                is_user_liked_for_post = True
            else:
                is_user_liked_for_post = False
            is_user_liked_for_posts.append(is_user_liked_for_post)

        context['postlike_count'] = postlike_counts
        context['is_user_liked_for_post'] = is_user_liked_for_posts

        return context
    
class PostDetailView(DetailView):
    model = Post
    template_name = 'postDetail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        post = self.get_object()  # ポストを取得
        post.views += 1  # viewsを1増やす
        post.save()  # データベースに保存

        postlike_count = self.object.postlike_set.count()
        # ポストに対するイイね数
        context['postlike_count'] = postlike_count
        # ログイン中のユーザーがイイねしているかどうか
        if self.object.postlike_set.filter(user=self.request.user).exists():
            context['is_user_liked_for_post'] = True
        else:
            context['is_user_liked_for_post'] = False

        return context

# class PostCreateView(LoginRequiredMixin, CreateView):
#     model = Post
#     fields = ['title', 'content', 'image', 'category']
#     template_name = 'post_create.html'
#     success_url = reverse_lazy('MyApp:post')
    
#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)

class PostCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'post_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(author=self.request.user)
        context['form'] = PostForm()

        postlike_counts = []
        is_user_liked_for_posts = []
        for post in context['posts']:
            postlike_count = post.postlike_set.count()
            postlike_counts.append(postlike_count)
            
            if post.postlike_set.filter(user=self.request.user).exists():
                is_user_liked_for_post = True
            else:
                is_user_liked_for_post = False
            is_user_liked_for_posts.append(is_user_liked_for_post)

        context['postlike_count'] = postlike_counts
        context['is_user_liked_for_post'] = is_user_liked_for_posts

        return context

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('MyApp:post')
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)

from django.views import View

class PostJsonView(View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        data = list(posts.values())
        return JsonResponse(data, safe=False)
    

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

#-----Talk-------

class TalkView(ListView):
    model = Talk
    template_name = 'talk.html'
    context_object_name = 'talks'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if 'popularity' in self.request.GET:
            queryset = queryset.annotate(num_likes=Count('talklike')).order_by('-num_likes')
        else:
            queryset = queryset.order_by('-date_posted')
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        talklike_counts = []
        is_user_liked_for_talks = []
        for talk in context['talks']:
            talklike_count = talk.talklike_set.count()
            talklike_counts.append(talklike_count)

            if talk.talklike_set.filter(user=self.request.user).exists():
                is_user_liked_for_talk = True
            else:
                is_user_liked_for_talk = False
            is_user_liked_for_talks.append(is_user_liked_for_talk)

        context['talklike_counts'] = talklike_counts
        context['is_user_liked_for_talks'] = is_user_liked_for_talks

        return context


class TalkDetailView(DetailView):
    model = Talk
    template_name = 'talkDetail.html'
    context_object_name = 'talk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        talk = self.get_object()  # ポストを取得
        talk.views += 1  # viewsを1増やす
        talk.save()  # データベースに保存

        talklike_count = self.object.talklike_set.count()
        # ポストに対するイイね数
        context['talklike_count'] = talklike_count
        # ログイン中のユーザーがイイねしているかどうか
        if self.object.talklike_set.filter(user=self.request.user).exists():
            context['is_user_liked_for_talk'] = True
        else:
            context['is_user_liked_for_talk'] = False

        return context

class TalkCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'talk_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['talks'] = Talk.objects.filter(author=self.request.user)
        context['form'] = TalkForm()

        talklike_counts = []
        is_user_liked_for_talks = []
        for talk in context['talks']:
            talklike_count = talk.talklike_set.count()
            talklike_counts.append(talklike_count)

            if talk.talklike_set.filter(user=self.request.user).exists():
                is_user_liked_for_talk = True
            else:
                is_user_liked_for_talk = False
            is_user_liked_for_talks.append(is_user_liked_for_talk)

        context['talklike_counts'] = talklike_counts
        context['is_user_liked_for_talks'] = is_user_liked_for_talks

        return context

    def post(self, request, *args, **kwargs):
        form = TalkForm(request.POST)
        if form.is_valid():
            talk = form.save(commit=False)
            talk.author = request.user
            talk.save()
            return redirect('MyApp:talk')
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)


@require_POST
@login_required
def talk_like(request):
    talk_pk = request.POST.get('talk_pk')
    context = {
        'user': f'{ request.user }',
    }
    talk = get_object_or_404(Talk, pk=talk_pk)
    like = TalkLike.objects.filter(talk=talk, user=request.user)

    if like.exists():
        like.delete()
        context['method'] = 'delete'
    else:
        like.create(talk=talk, user=request.user)
        context['method'] = 'create'

    context['talklike_count'] = talk.talklike_set.count()

    return JsonResponse(context)

#----------------MyPage----------------------

class MyPageView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'myPage.html'
    context_object_name = 'profiles'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['posts'] = Post.objects.filter(author=profile.user)
        return context

class MyPageCreateView(LoginRequiredMixin, CreateView):
    model = Profile
    fields = ['name','icon','bio','age','gender','university','sns_account','hobby','language']
    template_name = 'myPage_create.html'
    
    def get_success_url(self):
        return reverse_lazy('MyApp:myPage', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    
class MyPageUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['name', 'icon', 'bio', 'age', 'gender', 'university', 'sns_account', 'hobby', 'language']
    template_name = 'myPage_update.html'

    def get_success_url(self):
        return reverse_lazy('MyApp:myPage', kwargs={'pk': self.object.pk})

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset.filter(user=self.request.user)

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        obj = queryset.get(user=self.request.user)
        return obj

class MyPageJsonView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        posts = Post.objects.filter(author=user)
        data = list(posts.values())
        return JsonResponse(data, safe=False)

#----------------------------------

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
