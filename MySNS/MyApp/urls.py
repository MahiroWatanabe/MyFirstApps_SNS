from django.urls import path
from django.views.generic import RedirectView
from django.contrib.auth.views import LoginView, LogoutView

from .views import UserPostListView

urlpatterns = [
    path('', RedirectView.as_view(url='index/', permanent=True)),
    path('index/', UserPostListView.as_view(), name="index"),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    # path("detail/<int:pk>", detailfunc, name='detail'),
    # path("good/<int:pk>", goodfunc, name='good'),
    # path("read/<int:pk>", readfunc, name='read'),
    # path("create/", BoardCreate.as_view(), name='create'),
]
