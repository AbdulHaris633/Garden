from django.urls import path
from gardening.views import * 
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView  

urlpatterns = [  
    # path('user/edit/', UserEditView.as_view(), name='user-edit'),
    # path('user/delete/', UserDeleteView.as_view(), name='user-delete'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('create-region/', RegionCreateView.as_view(), name='create-region'),
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categorie/', CategoryCreateView.as_view(), name='category-create'),
    path('category/products/', CategoryProductView.as_view(), name='category-detail'),
    path('report-problem/', ReportProblemView.as_view(), name='report-problem'),
    path('products/create/', CreateProductView.as_view(), name='create-product'),
    path('product/delete/', CreateProductView.as_view(), name='product-delete'),
    path('regions/products/', UserRegionProductView.as_view(), name='get-products-by-region'), 
    path('upload-image/', UserImagesView.as_view(), name='upload-image'),
    path('user-images/', ListUserImagesView.as_view(), name='user-images'),
    path('create-post/', CreatePostView.as_view(), name='create-post'),
    path('posts/', ListPostsView.as_view(), name='posts'),
    path('articles/create/', ArticleCreateAPIView.as_view(), name='article-create'),
    path('articles/', ArticleListAPIView.as_view(), name='article-list'),
    path('garden/create/', CreateGardenView.as_view(), name='create_garden'),
    path('garden/add-products/', AddProductsToGardenView.as_view(), name='add_products_to_garden'),
    path('garden/products/', GetGardenProductsView.as_view(), name='get-garden-products'),
    path('chat/', ChatGPTView.as_view(), name='chat_gpt'),
]


