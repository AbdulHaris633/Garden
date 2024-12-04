from django.shortcuts import render
import json
import openai

# third parties imports
from django.contrib.auth import authenticate
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db import transaction

# app imports
from .models import *
from .serializers import *
from gardening.models import Region
from gardening.serializers import RegionSerializer 



class UserRegisterView(APIView):
    # permission_classes = [permissions.AllowAny]   

    def get(self, request, *args, **kwargs):
       
        regions = Region.objects.all()
        region_serializer = RegionSerializer(regions, many=True)
        return Response({"regions": region_serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)

        if serializer.is_valid():
            validated_data = serializer.validated_data
            region = validated_data.pop('region')
            password = validated_data.pop('password')
            confirm_password = validated_data.pop('confirm_password')

            if password != confirm_password:
                return Response({'detail': 'Passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)

            user = User(**validated_data) 
            user.set_password(password)  
            if region:
                try:
                    region = Region.objects.get(id=region)
                    user.region = region
                    user.save()
                except Region.DoesNotExist:
                    return Response({'detail': 'Invalid region ID provided.'}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"detail": "User registered successfully."}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserLoginView(APIView):
    # permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        print('user')
        serializer.is_valid(raise_exception=True) 
        print('user')

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        user = authenticate(username=username, password=password)
        print(user)
        if user:
            refresh = RefreshToken.for_user(user)
            user_data = UserSerializer(user).data
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': user_data 
            })
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)