from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from common.serializer import (
    OperationError,
    OperationSuccess,
)
from common.pagination import CustomPagination
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
)
from assigner.api.serializers.accounts import AccountsCreateSerializer
from assigner.models import User


@extend_schema_view(
    post=extend_schema(
        summary="Refer to Schemas At Bottom",
        description="User Account Registration Apis",
        request=AccountsCreateSerializer,
        responses={
            200: OpenApiResponse(
                response=OperationSuccess,
                description="Success Response when user is registered successfully",
            ),
            422: OpenApiResponse(
                response=OperationError,
                description="Json Data Error, occurs when invalid data is sent!",
            ),
        },
        tags=["User Unauthenticated Apis"],
    ),
)
class AccountsCreateViewSet(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = AccountsCreateSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {
                "title": "Accounts",
                "message": "Accounts created successfully",
                "data": response.data,
            }
        )
