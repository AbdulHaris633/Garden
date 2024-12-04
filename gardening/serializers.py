from rest_framework import serializers
from .models import * 


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'  



class ProductSerializer(serializers.ModelSerializer):
    region_id = serializers.UUIDField(write_only=True) 
    class Meta:
        model = Product
        fields = (
            'name', 
            'description', 
            'image', 
            'days_to_maturity', 
            'mature_speed', 
            'mature_height', 
            'fruit_size', 
            'family',
            'type', 
            'native', 
            'hardiness',
            'exposure', 
            'plant_dimension', 
            'variety_info',
            'attributes', 
            'category', 
            'region_id'
        )


class CategorySerializer(serializers.ModelSerializer):
    # products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = '__all__'


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportAProblem
        fields = ['id', 'description', 'image', 'user', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['id', 'image', 'user']


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'image', 'description', 'user', 'created_at']
        read_only_fields = ['id', 'user', 'created_at'] 


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'description', 'image', 'article_link', 'user', 'created_at']
        read_only_fields = ['user', 'created_at']



class GardenCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Garden
        fields = ['id', 'user', 'created_at']
        read_only_fields = ['id', 'created_at']

    # def create(self, validated_data):
    #     return Garden.objects.create(**validated_data)


class GardenAddProductSerializer(serializers.Serializer):
    product_ids = serializers.ListField(
        child=serializers.UUIDField(), allow_empty=False
    )

    def validate_product_ids(self, product_ids):
        """
        Validate that all provided product IDs exist in the database.
        """
        existing_products = Product.objects.filter(id__in=product_ids)
        if existing_products.count() != len(product_ids):
            raise serializers.ValidationError("Some products do not exist.")
        return product_ids
    

class GardenProductSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name')
    product_description = serializers.CharField(source='product.description')

    class Meta:
        model = GardenProduct
        fields = ['id', 'product_name', 'product_description', 'quantity', 'date_added']
    
    
class ChatBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatBox
        fields = ['id', 'question', 'answer', 'user', 'created_at']
        read_only_fields = ['id', 'answer', 'created_at', 'user']
