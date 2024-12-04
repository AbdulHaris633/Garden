# Built-in imports
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

    

class RegionCreateView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # if not request.user.is_superuser:
        #     return Response({'detail': 'Only superusers can create regions.'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = RegionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryListCreateView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        print(categories)
        print("2222222")
        return Response(serializer.data) 
        
    

class CategoryCreateView(APIView):
    def post(self, request):
        print("1111111")
        serializer = CategorySerializer(data=request.data)
        print("2222222")
        if serializer.is_valid():
            print("1111111")
            serializer.save()
            print("22222")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        
        print("1111111")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryProductView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data 
        print("11111")
        category_id = data.get('category_id')
        print("22222")
        if not category_id:
            return Response({"error": "category_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            products_qs = Product.objects.filter(category_id=category_id)
            print("11111")
            serializer = ProductSerializer(products_qs, many=True)
            return Response(serializer.data)
        except Category.DoesNotExist:
            return Response({"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND)


class ReportProblemView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ReportSerializer(data=request.data)
        print("22222")
        if serializer.is_valid():
            report = serializer.save(user=request.user)
            print("22222")
            subject = f"New Problem Report from {report.user.username}"
            print("22222")
            message = f"Description: {report.description}\nImage URL: {report.image.url}\nReported by: {report.user.username}\nCreated at: {report.created_at}"
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [settings.REPORT_EMAIL]
            send_mail(subject, message, from_email, recipient_list)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#  ///////////////////////////////////////
class CreateProductView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = ProductSerializer(data=request.data)
        
        if serializer.is_valid():
            validated_data = serializer.validated_data
            product = Product.objects.create(**validated_data)
            
            region_id = validated_data.pop('region_id', None)

            try:
                if region_id:
                    region = Region.objects.get(id=region_id)
                    print("22222")  
                    product.region.set([region]) 
                return Response(
                    {"detail": "Product created and assigned successfully.", "product_id": str(product.id)},
                    status=status.HTTP_201_CREATED
                )
            except Region.DoesNotExist:
                return Response({'detail': 'Invalid region ID provided.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        print("22222")
        if not product_id:
            return Response({"detail": "Product ID not provided."}, status=status.HTTP_400_BAD_REQUEST)
        print("22222")
        product = get_object_or_404(Product, id=product_id)
        print("22222")
        product.delete()
        return Response({"detail": "Product deleted successfully."}, status=status.HTTP_204_NO_CONTENT)



class UserRegionProductView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user_region_id = request.user.region_id  
            products_qs = Product.objects.filter(region__id=user_region_id)
            serializer = ProductSerializer(products_qs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except AttributeError:
            return Response({"error": "User does not have a region assigned."}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class UserImagesView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # if not request.user or not request.user.is_authenticated:
        #     return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)
        print("22222")
        image_data = request.data.get('image')
        print("22222")
        if not image_data:
            return Response({"error": "Image field is required."}, status=status.HTTP_400_BAD_REQUEST)
        print("22222")
        image = Images.objects.create(user=request.user, image=image_data)
        print("22222")
        serializer = ImagesSerializer(image)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ListUserImagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        images = Images.objects.filter(user=request.user)
        serializer = ImagesSerializer(images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreatePostView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListPostsView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        posts = Post.objects.all().order_by('-created_at')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ArticleCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if not request.user.is_superuser:
            return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class ArticleListAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
    

class CreateGardenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        if hasattr(user, 'garden_user'):
            return Response({"error": "User already has a garden."}, status=status.HTTP_400_BAD_REQUEST)

        garden_data = {'user': user.id}
        serializer = GardenCreateSerializer(data=garden_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class AddProductsToGardenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        try:
            garden = user.garden_user
        except Garden.DoesNotExist:
            return Response({"error": "User does not have a garden."}, status=status.HTTP_404_NOT_FOUND)

        serializer = GardenAddProductSerializer(data=request.data)
        if serializer.is_valid():

            product_ids = serializer.validated_data['product_ids']
            self.add_products_to_garden(garden, product_ids)
            return Response({"success": "Products added successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def add_products_to_garden(self, garden, product_ids):
        """
        Adds products to the garden, allowing duplicates by creating separate GardenProduct entries.
        """
        for product_id in product_ids:
            product = Product.objects.get(id=product_id)
            GardenProduct.objects.create(garden=garden, product=product)
            print(f"Added {product.name} to {garden.user.username}'s garden.")


class GetGardenProductsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        try:
            garden = user.garden_user 
        except Garden.DoesNotExist:
            return Response({"error": "User does not have a garden."}, status=status.HTTP_404_NOT_FOUND)

        garden_products = GardenProduct.objects.filter(garden=garden)
        serializer = GardenProductSerializer(garden_products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



    
class ChatGPTView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        question = request.data.get('question')

        if not question:
            return JsonResponse({"error": "Question is required"}, status=400)

        try:
            # Set the OpenAI API key
            openai.api_key = settings.OPENAI_API_KEY

            # Use the GPT-3.5 model instead of GPT-4
            response = openai.completions.create(
                model="gpt-3.5-turbo",  # Use GPT-3.5 here
                prompt=question,
                max_tokens=200  # Adjust token limit as needed
            )

            # Extract GPT's response
            answer = response['choices'][0]['text']

            # Save chat to the database
            chat = ChatBox.objects.create(
                user=user,
                question=question,
                answer=answer
            )

            # Serialize and return the response
            serializer = ChatBoxSerializer(chat)
            return JsonResponse(serializer.data, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
