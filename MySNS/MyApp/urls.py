from django.urls import path
from django.views.generic import RedirectView
from django.contrib.auth.views import LoginView, LogoutView

from .views import UserPostListView, TalkView, PostView, MyPageView, PostDetailView, TalkDetailView, SignupView
from .views import post_like, login_signup

app_name = 'MyApp'

urlpatterns = [
    path('', RedirectView.as_view(url='index/', permanent=True)),

    path('index/', UserPostListView.as_view(), name="index"),

    path('talk/', TalkView.as_view(), name="talk"),
    path('talk/<int:pk>/', TalkDetailView.as_view(), name='post_detail'),

    path('post/', PostView.as_view(), name="post"),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post_like/', post_like, name='post_like'),
    
    path('myPage/', MyPageView.as_view(), name="myPage"),

    path('signup/', SignupView.as_view(), name='signup'),

    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='MyApp:login'), name='logout'),

    path('login_signup/', login_signup, name='login_signup'),

    # path("detail/<int:pk>", detailfunc, name='detail'),
    # path("good/<int:pk>", goodfunc, name='good'),
    # path("read/<int:pk>", readfunc, name='read'),
    # path("create/", BoardCreate.as_view(), name='create'),
]
