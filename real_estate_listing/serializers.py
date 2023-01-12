from rest_framework import serializers

from users.serializers import UserListSerializer, UserSerializer

from .models import RealEstateItem


class RealEstateItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = RealEstateItem
        fields = "__all__"


# class RealEstateItemGetSerializer(serializers.ModelSerializer):
#     user = UserSerializer(source="created_by", read_only=True)
#
#     class Meta:
#         model = RealEstateItem
#         fields = "__all__"
