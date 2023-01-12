
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication


from .models import RealEstateItem
from .serializers import (
    RealEstateItemSerializer,
)
from .utils import realestate_gs_marker


class LCRealEstateItemViewSet(ListCreateAPIView):
    serializer_class = RealEstateItemSerializer
    queryset = RealEstateItem.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    @swagger_auto_schema(tags=["RealEstateItems"])
    def get(self, request, *args, **kwargs):
        query_set = RealEstateItem.objects.filter(created_by=request.user.id)
        serializer = self.get_serializer(query_set, many=True)
        return Response(serializer.data)


    @swagger_auto_schema(tags=["RealEstateItems"])
    def post(self, request, *args, **kwargs):
        request.data["created_by"] = request.user.id
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError:
            error_list = [
                serializer.errors[error][0].replace("This", error)
                for error in serializer.errors
            ]
            return Response({"errors": error_list}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)

        real_est_item = RealEstateItem.objects.get(pk=serializer.data["id"])
        real_est_item.save()

        response = RealEstateItemSerializer(real_est_item).data
        headers = self.get_success_headers(serializer.data)
        realestate_gs_marker.now(response)
        return Response(
            response, status=status.HTTP_201_CREATED, headers=headers
        )


class RUDRealEstateItemViewSet(RetrieveUpdateDestroyAPIView):
    http_method_names = ["get", "patch", "delete"]
    serializer_class = RealEstateItemSerializer
    queryset = RealEstateItem.objects.all()

    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    @swagger_auto_schema(tags=["RealEstateItems"])
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=["RealEstateItems"])
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        try:
            # instance = get_sop_queryset(request).get(pk=kwargs["pk"])
            instance = self.get_object()
        except RealEstateItem.DoesNotExist:
            return Response(
                {"errors": ["RealEstateItem does not exists"]}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    @swagger_auto_schema(tags=["RealEstateItems"])
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if (
                instance.created_by == request.user
        ):
            response = RealEstateItemSerializer(instance).data
            self.perform_destroy(instance)
            return Response(response, status=status.HTTP_202_ACCEPTED)
        elif instance.created_by != request.user:
            return Response(
                {"errors": ["You can not delete any other Owner’s RealEstateItem"]},
                status=status.HTTP_400_BAD_REQUEST,
            )

