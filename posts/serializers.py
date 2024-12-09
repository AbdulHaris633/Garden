from rest_framework import serializers
from .models import *

class PostSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    user = serializers.CharField(required=False)
    
    class Meta:   
         model = Post
         fields = "__all__" 