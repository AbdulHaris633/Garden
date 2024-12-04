from django.urls import path
from users.views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView  

urlpatterns = [  
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login') 
]    