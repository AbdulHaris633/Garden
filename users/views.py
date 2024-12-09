from django.shortcuts import render
from .models import*
from .serializers import*
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from plant.models import Product,ProductRegion
from plant.serializers import ProductSerializer
from .models import User,UserRegion,Region
from .serializers import UserRegionProductSerialzier
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny


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
            
            
            # request_user = serializer.validated_data.get("username")
            
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
             