from allauth.account.utils import send_email_confirmation
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.conf import settings
from rest_framework import serializers

from .models import *


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = "__all__"


class UserRegionProductSerialzier(serializers.Serializer):
    username = serializers.CharField(max_length=30, required=False)


class CustomRegisterSerializer(RegisterSerializer):
    email = serializers.EmailField(required=True)

    def custom_signup(self, request, user):
        user.email = self.validated_data.get("email")
        user.save()

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already in use.")
        return value
