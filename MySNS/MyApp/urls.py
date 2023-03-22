from django.urls import path
from django.views.generic import RedirectView

from .views import UserPostListView

urlpatterns = [
    path('', RedirectView.as_view(url='index/', permanent=True)),
    path('index/', UserPostListView.as_view(), name="index")
]
