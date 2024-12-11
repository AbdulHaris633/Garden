from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from plant.models import Product, ProductRegion
from plant.serializers import ProductSerializer
from django.core.mail import send_mail

from .models import *
from .models import Region, User, UserRegion
from .serializers import *
from .serializers import UserRegionProductSerialzier
from .serializers import CustomRegisterSerializer
from dj_rest_auth.registration.views import RegisterView
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

from dj_rest_auth.registration.views import RegisterView


class RegionCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RegionSerializer
    queryset = Region.objects.all()


class RegionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = RegionSerializer
    queryset = Region.objects.all() 
    lookup_field = "id"


class GetProductsByUserRegion(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserRegionProductSerialzier

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            username_ = request.user

            try:
                region = UserRegion.objects.get(user__username=username_).region
            except:
                return Response({"message": "Region not found for this user."})

            try:
                product_regions = ProductRegion.objects.filter(region=region)
            except:
                return Response({"message": "Product Region not found."})

            products = []

            for obj in product_regions:
                products.append(obj.product)

            product_serializer = ProductSerializer(products, many=True)

            return Response(product_serializer.data)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomRegisterView(RegisterView): 
    serializer_class = CustomRegisterSerializer 

    def perform_create(self, serializer):
        user = super().perform_create(serializer)
        email = serializer.validated_data.get("email") 
        user.email = email
        user.save()   
        return user  
    