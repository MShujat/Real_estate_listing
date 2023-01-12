"""All the views related to users exist here."""
import datetime
import logging
from datetime import timezone

from django.contrib.auth import get_user_model, password_validation
from django_rest_passwordreset.views import (
    ResetPasswordConfirm,
    ResetPasswordRequestToken,
    ResetPasswordValidateToken,
)
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenViewBase

from users.serializers import (
    UserRegisterSerializer,
    UserSerializer,
    UserListSerializer,
    UserUpdateSerializer
)

UserModel = get_user_model()
logger = logging.getLogger(__name__)


class UserRegisterViewSet(viewsets.ViewSet):
    """Viewset responsible for registering the user."""

    permission_classes = (IsAuthenticated, IsAdminUser)
    authentication_classes = (JWTAuthentication,)

    @swagger_auto_schema(
        method="post",
        request_body=UserRegisterSerializer(),
    )
    @action(
        detail=False,
        methods=["post"],
    )
    def register_user(self, request):
        """Register User."""
        serializer = UserRegisterSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            password_validation.validate_password(serializer.validated_data["password"])
        except ValidationError as e:
            logger.error(e)
            if serializer.errors:
                error_list = [
                    serializer.errors[error][0].replace("This", error)
                    for error in serializer.errors
                ]
                return Response(
                    {"errors": error_list}, status=status.HTTP_400_BAD_REQUEST
                )
            else:
                return Response(
                    {"errors": e.args}, status=status.HTTP_412_PRECONDITION_FAILED
                )
        except Exception as e:
            return Response(
                {"errors": e}, status=status.HTTP_412_PRECONDITION_FAILED
            )
        user = UserModel.objects.create(
            first_name=serializer.validated_data["first_name"],
            last_name=serializer.validated_data["last_name"],
            email=serializer.validated_data["email"],
            address=serializer.validated_data["address"],
            phone_number=serializer.validated_data["phone_number"],
        )
        user.set_password(serializer.validated_data["password"])
        user.save()

        return Response(status=status.HTTP_200_OK, data=UserSerializer(user).data)


class UserUpdateViewSet(viewsets.ViewSet):
    """Viewset responsible for updating the user."""

    permission_classes = (IsAuthenticated, IsAdminUser)
    authentication_classes = (JWTAuthentication,)

    @swagger_auto_schema(
        method="post",
        request_body=UserUpdateSerializer(),
    )
    @action(
        detail=False,
        methods=["post"],
    )
    def partial_update(self, request, pk=None):
        """Register User."""
        instance = UserModel.objects.get(id=pk)
        serializer = UserUpdateSerializer(instance, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            logger.error(e)
            if serializer.errors:
                error_list = [
                    serializer.errors[error][0].replace("This", error)
                    for error in serializer.errors
                ]
                return Response(
                    {"errors": error_list}, status=status.HTTP_400_BAD_REQUEST
                )
            else:
                return Response(
                    {"errors": e.args}, status=status.HTTP_412_PRECONDITION_FAILED
                )
        except Exception as e:
            return Response(
                {"errors": e}, status=status.HTTP_412_PRECONDITION_FAILED
            )
        serializer.save()
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class UserViewSet(viewsets.ViewSet):
    """Viewset that creates the Apis for listing and retrieving the users."""

    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    @swagger_auto_schema(tags=["Users"])
    def list(self, request):
        """List all the users in the DB."""
        queryset = UserModel.objects.all()
        serializer = UserListSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(tags=["Users"])
    def retrieve(self, request, pk=None):
        """Retrieve a user using the primary key."""
        queryset = UserModel.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class TokenObtainUserSerializer(TokenObtainPairSerializer):
    """User login serializer."""

    def validate(self, attrs):
        """Validate the user and return the user instance and access token if user is valid."""
        self.error_messages["no_active_account"] = {
            "errors": ["No user found with the given credentials"]
        }
        data = super().validate(attrs)
        self.user.login_count = self.user.login_count + 1
        self.user.save()
        data["token"] = {"access": data["access"], "refresh": data["refresh"]}
        del data["access"]
        del data["refresh"]
        data["user"] = UserSerializer(self.user).data
        self.user.last_login = datetime.datetime.now(tz=timezone.utc)
        return data


class TokenObtainUserView(TokenViewBase):
    """API for user login."""

    serializer_class = TokenObtainUserSerializer

    def post(self, request, *args, **kwargs):
        """Request Login."""

        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        except ValidationError as e:
            error_list = [
                serializer.errors[error][0].replace("This", error)
                for error in serializer.errors
            ]
            return Response({"errors": error_list}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class CustomResetPasswordRequestToken(ResetPasswordRequestToken):
    """API for user Reset Password."""

    def post(self, request, *args, **kwargs):
        """Request for Password Rest."""
        try:
            response = super().post(request, *args, **kwargs)
        except ValidationError as e:
            error_list = []
            if "email" in e.args[0]:
                error_message = e.args[0]["email"]
                error_list.append(error_message[0].replace("This", "email"))

            return Response({"errors": error_list}, status=status.HTTP_400_BAD_REQUEST)

        return response


class CustomResetPasswordValidateToken(ResetPasswordValidateToken):
    """API for validating the reset password."""

    def post(self, request, *args, **kwargs):
        """Request for reset password token validation."""
        try:
            response = super().post(request, *args, **kwargs)
        except ValidationError as e:
            error_list = []
            if "token" in e.args[0]:
                error_message = e.args[0]["token"]
                error_list.append(error_message[0].replace("This", "token"))
            return Response({"errors": error_list}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"errors": e.args}, status=status.HTTP_400_BAD_REQUEST)

        return response


class CustomResetPasswordConfirm(ResetPasswordConfirm):
    """Confirm change password using reset token."""

    def post(self, request, *args, **kwargs):
        """If token is valid reset the password to new password."""
        try:
            response = super().post(request, *args, **kwargs)
        except ValidationError as e:
            error_list = []
            if "token" in e.args[0]:
                error_message = e.args[0]["token"]
                error_list.append(error_message[0].replace("This", "token"))
            if "password" in e.args[0]:
                error_message = e.args[0]["password"]
                error_list.append(error_message[0].replace("This", "password"))
            return Response({"errors": error_list}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"errors": e.args}, status=status.HTTP_400_BAD_REQUEST)

        return response

