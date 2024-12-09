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
     
     def post(self, request, *args, **kwargs):
          serializer = self.get_serializer(data=request.data) 
            
          if serializer.is_valid(): 
               req_user = request.user
               description = serializer.validated_data.get("description")

               try:
                    user = User.objects.get(username=req_user)
               except User.DoesNotExist:
                    return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

               try:
                    Post.objects.create(description=description, user=user)
                    return Response({"message": "Post created successfully"}, status=status.HTTP_201_CREATED)
               except:
                    return Response({"message": "Error while creating Post."})
          
          else:
               return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)     
                
               