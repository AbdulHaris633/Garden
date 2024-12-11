from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import * 
from allauth.account.utils import send_email_confirmation
from django.conf import settings



class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = "__all__"


class UserRegionProductSerialzier(serializers.Serializer):
    username = serializers.CharField(max_length=30, required=False)


class CustomRegisterSerializer(RegisterSerializer): 
    email = serializers.EmailField(required=True)

    def custom_signup(self, request, user):
        user.email = self.validated_data.get('email') 
        user.save() 

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already in use.") 
        return value
    


