from django.urls import path
from posts.views import*
urlpatterns = [
    path("userpost/", PostListCreateAPIView.as_view())    
]  