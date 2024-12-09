from django.shortcuts import render
from  .models import Post
from .serializers import*
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from users.models import User

class PostListCreateAPIView(generics.ListCreateAPIView):
     permission_classes = [IsAuthenticated]
     serializer_class = PostSerializer 
     queryset = Post.objects.all()  
     
