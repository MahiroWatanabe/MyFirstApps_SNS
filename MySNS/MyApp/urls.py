from django.urls import path
from django.views.generic import RedirectView
from django.contrib.auth.views import LoginView, LogoutView

from .views import MyPageUpdateView, PostJsonView, UserPostListView, TalkView, PostView, MyPageView, PostDetailView, TalkDetailView, SignupView, PostCreateView, TalkCreateView, MyPageCreateView, MyPageJsonView
from .views import post_like, talk_like, login_signup

app_name = 'MyApp'

urlpatterns = [
    path('', RedirectView.as_view(url='index/', permanent=True)),

    path('index/', UserPostListView.as_view(), name="index"),

    path('talk/', TalkView.as_view(), name="talk"),
    path('talk/create', TalkCreateView.as_view(), name="talk_create"),
    path('talk/<int:pk>/', TalkDetailView.as_view(), name='talk_detail'),
    path('talk_like/', talk_like, name='talk_like'),

    path('post/', PostView.as_view(), name="post"),
    path('post/create', PostCreateView.as_view(), name="post_create"),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post_like/', post_like, name='post_like'),
    path('post/json/', PostJsonView.as_view(), name='post_json'),
    
    path('myPage/create', MyPageCreateView.as_view(), name="myPage_create"),
    path('myPage/<int:pk>/update', MyPageUpdateView.as_view(), name="myPage_update"),
    path('myPage/<int:pk>', MyPageView.as_view(), name="myPage"),
    path('myPage/json/', MyPageJsonView.as_view(), name='post_json'),

    path('signup/', SignupView.as_view(), name='signup'),

    # path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('login/', login_signup, name='login'),
    path('logout/', LogoutView.as_view(next_page='MyApp:login'), name='logout'),

    path('login_signup/', login_signup, name='login_signup'),

    # path("detail/<int:pk>", detailfunc, name='detail'),
    # path("good/<int:pk>", goodfunc, name='good'),
    # path("read/<int:pk>", readfunc, name='read'),
    # path("create/", BoardCreate.as_view(), name='create'),
]
