from django.contrib.auth import get_user_model
from rest_framework import serializers

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer to get user instance."""

    class Meta:
        """Exclude password when serializing users."""

        model = UserModel
        fields = ["id", "first_name", "last_name", "email", "address", "phone_number", "login_count"]


class UserListSerializer(serializers.ModelSerializer):
    """Serializer to get user instance."""

    class Meta:
        """Exclude password when serializing users."""

        model = UserModel
        fields = ["id", "first_name", "last_name", "email", "address", "phone_number"]


class UserRegisterSerializer(serializers.ModelSerializer):
    """Serializer to register user."""

    class Meta:
        """Fields required when registering the user."""

        model = UserModel
        fields = ["id", "email", "password", "first_name", "last_name", "address", "phone_number"]


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer to update user."""

    class Meta:
        """Fields required when registering the user."""

        model = UserModel
        fields = ["id", "first_name", "last_name", "address", "phone_number"]
