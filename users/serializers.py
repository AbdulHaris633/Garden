from rest_framework import serializers

from .models import *


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = "__all__"


class UserRegionProductSerialzier(serializers.Serializer):
    username = serializers.CharField(max_length=30, required=False)
