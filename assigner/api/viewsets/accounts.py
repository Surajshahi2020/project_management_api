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
    OpenApiExample,
)
from assigner.api.serializers.accounts import (
    AccountsCreateSerializer,
    AccountDetailSerializer,
    ProjectCreateSerializer,
    ProjectEditSerializer,
    TaskCreateSerializer,
    TaskEditSerializer,
    SubmitTaskSerializer,
    SubmitTaskEditSerializer,
)
from assigner.models import (
    User,
    Project,
    Task,
    SubmittedTask,
)
from assigner.api.serializers.accounts import LoginSerializer
from common.permissions import (
    IsHumanResource,
    IsAuthenticated,
    IsHrOrSupervisor,
)
from common.pagination import CustomPagination
from common.utils import validate_uuid
from common.exceptions import UnprocessableEntityException


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


@extend_schema_view(
    post=extend_schema(
        summary="Refer to Schema At Bottom",
        examples=[
            OpenApiExample(
                name="Login by email-email",
                request_only=True,
                value={"email": "kingshahi163@gmail.com", "password": "HIGHspeed12@"},
            ),
            OpenApiExample(
                name="Login by phone-phone",
                request_only=True,
                value={
                    "phone": "9809461773",
                    "password": "HIGHspeed12@",
                },
            ),
        ],
        description="Login Api",
        request=LoginSerializer,
        responses={
            200: OpenApiResponse(
                response=OperationSuccess,
                description="Success Response when Loggedin successfully",
            ),
            422: OpenApiResponse(
                response=OperationError,
                description="Json Data Error, occurs when invalid data is sent!",
            ),
        },
        tags=["User Unauthenticated Apis"],
    ),
)
class LoginViewSet(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if "email" in serializer.validated_data:
            user = User.objects.filter(email=serializer.validated_data["email"]).first()
        elif "phone" in serializer.validated_data:
            user = User.objects.filter(phone=serializer.validated_data["phone"]).first()
        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token
        return Response(
            {
                "title": "Login",
                "message": "Logged in successfully",
                "data": {
                    **AccountDetailSerializer(instance=user).data,
                    "access": str(access_token),
                    "refresh": str(refresh_token),
                },
            }
        )


@extend_schema_view(
    post=extend_schema(
        summary="Refer to Schemas At Bottom",
        description="Project Create Apis",
        request=ProjectCreateSerializer,
        responses={
            200: OpenApiResponse(
                response=OperationSuccess,
                description="Success Response when project is created successfully",
            ),
            422: OpenApiResponse(
                response=OperationError,
                description="Json Data Error, occurs when invalid data is sent!",
            ),
        },
        tags=["Project Apis"],
    ),
)
class ProjectCreateViewSet(generics.CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectCreateSerializer
    permission_classes = [IsHumanResource]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {
                "title": "Project",
                "message": "Project created successfully",
                "data": response.data,
            }
        )


@extend_schema_view(
    get=extend_schema(
        summary="Refer to Schemas At Bottom",
        description="Project List Apis",
        request=ProjectCreateSerializer,
        responses={
            200: OpenApiResponse(
                response=OperationSuccess,
                description="Success Response when project is listed successfully",
            ),
            422: OpenApiResponse(
                response=OperationError,
                description="Json Data Error, occurs when invalid data is sent!",
            ),
        },
        tags=["Project Apis"],
    ),
)
class ProjectListViewSet(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectCreateSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = [
        "get",
    ]
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response(
            {
                "title": "Project",
                "message": "Project Listed successfully",
                "data": response.data,
            }
        )


@extend_schema_view(
    patch=extend_schema(
        summary="Refer to Schemas At Bottom",
        description="Project Edit Apis",
        request=ProjectEditSerializer,
        responses={
            200: OpenApiResponse(
                response=OperationSuccess,
                description="Success Response when project is edit successfully",
            ),
            422: OpenApiResponse(
                response=OperationError,
                description="Json Data Error, occurs when invalid data is sent!",
            ),
        },
        tags=["Project Apis"],
    ),
)
class ProjectEditViewSet(generics.UpdateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectEditSerializer
    permission_classes = [IsHumanResource]
    http_method_names = [
        "patch",
    ]

    def partial_update(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]
        if not validate_uuid(pk):
            raise UnprocessableEntityException(
                {
                    "title": "Project",
                    "message": "Invalid UUID",
                },
                code=422,
            )
        if not Project.objects.filter(id=pk).exists():
            raise UnprocessableEntityException(
                {
                    "title": "Project",
                    "message": "Project does  not Found!",
                },
                code=422,
            )
        response = super().partial_update(request, *args, **kwargs)
        return Response(
            {
                "title": "Project",
                "message": "Project edited successfully",
                "data": response.data,
            }
        )


@extend_schema_view(
    post=extend_schema(
        summary="Refer to Schemas At Bottom",
        description="Project Create Apis",
        request=TaskCreateSerializer,
        responses={
            200: OpenApiResponse(
                response=OperationSuccess,
                description="Success Response when task is created successfully",
            ),
            422: OpenApiResponse(
                response=OperationError,
                description="Json Data Error, occurs when invalid data is sent!",
            ),
        },
        tags=["Task Apis"],
    ),
)
class TaskCreateViewSet(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer
    permission_classes = [IsHrOrSupervisor]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {
                "title": "Task",
                "message": "Task created successfully",
                "data": response.data,
            }
        )


@extend_schema_view(
    patch=extend_schema(
        summary="Refer to Schemas At Bottom",
        description="Task Edit Apis",
        request=TaskEditSerializer,
        responses={
            200: OpenApiResponse(
                response=OperationSuccess,
                description="Success Response when Task is edited successfully",
            ),
            422: OpenApiResponse(
                response=OperationError,
                description="Json Data Error, occurs when invalid data is sent!",
            ),
        },
        tags=["Task Apis"],
    ),
)
class TaskEditViewSet(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskEditSerializer
    permission_classes = [IsHrOrSupervisor]
    http_method_names = [
        "patch",
    ]

    def partial_update(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]
        if not validate_uuid(pk):
            raise UnprocessableEntityException(
                {
                    "title": "Task",
                    "message": "Invalid UUID",
                },
                code=422,
            )
        if not Task.objects.filter(id=pk).exists():
            raise UnprocessableEntityException(
                {
                    "title": "Task",
                    "message": "Task does  not exist!",
                },
                code=422,
            )
        response = super().partial_update(request, *args, **kwargs)
        return Response(
            {
                "title": "Task",
                "message": "Task edited successfully",
                "data": response.data,
            }
        )


@extend_schema_view(
    get=extend_schema(
        summary="Refer to Schemas At Bottom",
        description="Task List Apis",
        request=TaskCreateSerializer,
        responses={
            200: OpenApiResponse(
                response=OperationSuccess,
                description="Success Response when Task is listed successfully",
            ),
            422: OpenApiResponse(
                response=OperationError,
                description="Json Data Error, occurs when invalid data is sent!",
            ),
        },
        tags=["Task Apis"],
    ),
)
class TaskListViewSet(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = [
        "get",
    ]
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response(
            {
                "title": "Task",
                "message": "Task Listed successfully",
                "data": response.data,
            }
        )


@extend_schema_view(
    post=extend_schema(
        summary="Refer to Schemas At Bottom",
        description="Submit Task Apis",
        request=SubmitTaskSerializer,
        responses={
            200: OpenApiResponse(
                response=OperationSuccess,
                description="Success Response when task is submitted successfully",
            ),
            422: OpenApiResponse(
                response=OperationError,
                description="Json Data Error, occurs when invalid data is sent!",
            ),
        },
        tags=["Task Submit Apis"],
    ),
)
class SubmitTaskViewSet(generics.CreateAPIView):
    queryset = SubmittedTask.objects.all()
    serializer_class = SubmitTaskSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {
                "title": "Submit Task",
                "message": "Submit Task created successfully",
                "data": response.data,
            }
        )


@extend_schema_view(
    patch=extend_schema(
        summary="Refer to Schemas At Bottom",
        description="Submit Task Edit Apis",
        request=SubmitTaskEditSerializer,
        responses={
            200: OpenApiResponse(
                response=OperationSuccess,
                description="Success Response when Submitted Task is edited successfully",
            ),
            422: OpenApiResponse(
                response=OperationError,
                description="Json Data Error, occurs when invalid data is sent!",
            ),
        },
        tags=["Task Submit Apis"],
    ),
)
class SubmitTaskEditViewSet(generics.UpdateAPIView):
    queryset = SubmittedTask.objects.all()
    serializer_class = SubmitTaskEditSerializer
    permission_classes = [IsHrOrSupervisor]
    http_method_names = [
        "patch",
    ]

    def partial_update(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]
        if not validate_uuid(pk):
            raise UnprocessableEntityException(
                {
                    "title": "Task",
                    "message": "Invalid UUID",
                },
                code=422,
            )
        if not SubmittedTask.objects.filter(id=pk).exists():
            raise UnprocessableEntityException(
                {
                    "title": "Submit Task",
                    "message": "Submit Task does  not exist!",
                },
                code=422,
            )
        response = super().partial_update(request, *args, **kwargs)
        return Response(
            {
                "title": "Submit Task",
                "message": "Submit Task edited successfully",
                "data": response.data,
            }
        )


@extend_schema_view(
    get=extend_schema(
        summary="Refer to Schemas At Bottom",
        description="Task Submit List Apis",
        request=SubmitTaskSerializer,
        responses={
            200: OpenApiResponse(
                response=OperationSuccess,
                description="Success Response when Submitted Task is listed successfully",
            ),
            422: OpenApiResponse(
                response=OperationError,
                description="Json Data Error, occurs when invalid data is sent!",
            ),
        },
        tags=["Task Submit Apis"],
    ),
)
class TaskSubmitListViewSet(generics.ListAPIView):
    queryset = SubmittedTask.objects.all()
    serializer_class = SubmitTaskSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = [
        "get",
    ]
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response(
            {
                "title": "Submit Task",
                "message": "Submit Task Listed successfully",
                "data": response.data,
            }
        )
