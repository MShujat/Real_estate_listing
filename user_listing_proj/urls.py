"""sop_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from users.views import (
    CustomResetPasswordConfirm,
    CustomResetPasswordRequestToken,
    CustomResetPasswordValidateToken,
    TokenObtainUserView,
    UserRegisterViewSet,
    UserViewSet,
    UserUpdateViewSet
)
from real_estate_listing.views import (
    LCRealEstateItemViewSet, RUDRealEstateItemViewSet
)

from .utils import BothHttpAndHttpsSchemaGenerator


router = SimpleRouter()

admin.site.site_header = "Jaldi User Admin"
admin.site.site_title = "Jaldi Admin Portal"
admin.site.index_title = "Welcome to Jaldi Admin Portal"

schema_view = get_schema_view(
    openapi.Info(
        title="USER API",
        default_version="v1",
        description="API documentation for USER APP",
    ),
    public=True,
    generator_class=BothHttpAndHttpsSchemaGenerator,
)

urlpatterns = (
        [
            path("admin/", admin.site.urls),
            path("auth/login/", TokenObtainUserView.as_view(), name="token_obtain_pair"),
            path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
            path("auth/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
            path(
                "user/register/",
                UserRegisterViewSet.as_view({"post": "register_user"}),
                name="register_user",
            ),
            path(
                "user/fetch/",
                UserViewSet.as_view({"get": "list"}),
                name="all_user",
            ),
            path(
                "user/fetch/<int:pk>/",
                UserViewSet.as_view({"get": "retrieve"}),
                name="one_user",
            ),

            path(
                "user/update/<int:pk>/",
                UserUpdateViewSet.as_view({"post": "partial_update"}),
                name="update_user",
            ),
            path(
                "auth/password-reset/validate_token/",
                CustomResetPasswordValidateToken.as_view(),
                name="reset-password-validate",
            ),
            path(
                "auth/password-reset/confirm/",
                CustomResetPasswordConfirm.as_view(),
                name="reset-password-confirm",
            ),
            path(
                "auth/password-reset/",
                CustomResetPasswordRequestToken.as_view(),
                name="password_reset",
            ),
            path("accounts/", include("rest_framework.urls", namespace="rest_framework")),
            path("realestates/", LCRealEstateItemViewSet.as_view(),
                 name="realestate_list_create"),
            path(
                "realestates/<int:pk>/", RUDRealEstateItemViewSet.as_view(),
                name="realestate_retrieve_update",
            ),
            path(
                "swagger/",
                schema_view.with_ui("swagger", cache_timeout=0),
                name="schema-swagger-ui",
            ),

        ]
        # + router.urls
        # + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

)


# urlpatterns.extend(
#     [
#         re_path(
#             r"swagger(?P<format>\.json|\.yaml)$",
#             schema_view.without_ui(cache_timeout=0),
#             name="schema-json",
#         ),
#         path(
#             "swagger/",
#             schema_view.with_ui("swagger", cache_timeout=0),
#             name="schema-swagger-ui",
#         ),
#         path(
#             "redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
#         ),
#     ]
# )
