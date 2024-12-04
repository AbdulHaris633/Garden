from rest_framework import serializers
from .models import User




class UserSerializer(serializers.ModelSerializer): 
    class Meta:
        model = User
        fields = (
            'username',
            'last_name',
            'description', 
            'country', 
            'name_privacy',  
            'country_privacy', 
            'region'
        )



class UserRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    region = serializers.UUIDField(write_only=True)

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate_username(self, value):
        if not value:
            raise serializers.ValidationError("Username is required.")
        return value

    def validate_password(self, value):
        if not value:
            raise serializers.ValidationError("Password is required.")
        return value