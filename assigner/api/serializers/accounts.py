from rest_framework import serializers
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
import traceback

from assigner.models import (
    User,
    Project,
    Task,
    SubmittedTask,
)
from common.exceptions import UnprocessableEntityException
from common.utils import (
    validate_email,
    validate_password,
    validate_phone,
    validate_url,
    validate_uuid,
)


class AccountsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "full_name",
            "phone",
            "email",
            "gender",
            "date_of_birth",
            "profile_pic",
            "password",
            "role",
        ]

        extra_kwargs = {
            "id": {
                "read_only": True,
            },
            "password": {
                "write_only": True,
            },
        }

    def is_valid(self, *, raise_exception=False):
        data = self.initial_data
        if data.get("full_name") == "":
            raise UnprocessableEntityException(
                {
                    "title": "Accounts",
                    "message": "FullName is required fields!",
                }
            )

        if data.get("password") == "":
            raise UnprocessableEntityException(
                {
                    "title": "Accounts",
                    "message": "Password is required fields!",
                }
            )

        if not validate_password(data.get("password")):
            raise UnprocessableEntityException(
                {
                    "title": "Accounts",
                    "message": "Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character!",
                }
            )

        if not data.get("profile_pic") == "" and not validate_url(
            data.get("profile_pic")
        ):
            raise UnprocessableEntityException(
                {
                    "title": "Accounts",
                    "message": "Valid profile picture is required!",
                }
            )

        if data.get("phone") == "":
            raise UnprocessableEntityException(
                {
                    "title": "Accounts",
                    "message": "Phone is required field!",
                }
            )

        if data.get("email") == "":
            raise UnprocessableEntityException(
                {
                    "title": "Accounts",
                    "message": "Emaul is required field!",
                }
            )

        if not data.get("phone") == "" and not validate_phone(data.get("phone")):
            raise UnprocessableEntityException(
                {
                    "title": "Accounts",
                    "message": "Invalid phone number!",
                }
            )

        if not data.get("email") == "" and not validate_email(data.get("email")):
            raise UnprocessableEntityException(
                {
                    "title": "Accounts",
                    "message": "Invalid email!",
                }
            )

        if User.objects.filter(phone=data.get("phone")).exists():
            raise UnprocessableEntityException(
                {
                    "title": "Accounts",
                    "message": "Phone number already linked with another user!",
                },
            )

        if User.objects.filter(email=data.get("email")).exists():
            raise UnprocessableEntityException(
                {
                    "title": "Accounts",
                    "message": "Email already linked with another user!",
                },
            )
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user = super().create(validated_data)
        password = validated_data.get("password")
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, allow_null=True, allow_blank=True)
    phone = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    password = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    def is_valid(self, *, raise_exception=False):
        data = self.initial_data

        if "phone" in data:
            if not data.get("phone") == "" and not validate_phone(data.get("phone")):
                raise UnprocessableEntityException(
                    {
                        "title": "Login",
                        "message": "Valid Phone is required!",
                    }
                )

        if "email" in data:
            if not data.get("email") == "" and not validate_email(data.get("email")):
                raise UnprocessableEntityException(
                    {
                        "title": "Login",
                        "message": "Valid Email is required!",
                    }
                )

        if data.get("password") == "":
            raise UnprocessableEntityException(
                {
                    "title": "Login",
                    "message": "Password is required field!",
                }
            )

        if "email" in data:
            user = User.objects.filter(email=data.get("email")).first()
        elif "phone" in data:
            user = User.objects.filter(phone=data.get("phone")).first()
        if user is not None:
            if user.check_password(data.get("password")):
                if user.is_blocked:
                    raise UnprocessableEntityException(
                        {
                            "title": "Login",
                            "message": "Account has been blocked!",
                        }
                    )
                if not user.is_active:
                    raise UnprocessableEntityException(
                        {
                            "title": "Login",
                            "message": "Account is not activated yet!",
                        }
                    )

            else:
                raise UnprocessableEntityException(
                    {
                        "title": "Login",
                        "message": "Incorrect Password!",
                    }
                )
        else:
            raise UnprocessableEntityException(
                {
                    "title": "Login",
                    "message": "Email or Phone does not exist!",
                }
            )
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        return validated_data


class AccountDetailSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    gender = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "full_name",
            "phone",
            "email",
            "gender",
            "role",
            "date_of_birth",
            "profile_pic",
        ]
        extra_kwargs = {
            "role": {
                "read_only": True,
            },
            "gender": {
                "read_only": True,
            },
        }

    @extend_schema_field(OpenApiTypes.STR)
    def get_role(self, obj):
        return obj.get_role_display()

    @extend_schema_field(OpenApiTypes.STR)
    def get_gender(self, obj):
        return obj.get_gender_display()


class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "description",
            "contributors",
            "status",
        ]

    def is_valid(self, *, raise_exception=False):
        data = self.initial_data
        if data.get("name") == "" or data.get("name") is None:
            raise UnprocessableEntityException(
                {
                    "title": "Project",
                    "message": "Name is required and cannot be empty.",
                }
            )

        if data.get("description") == "" or data.get("description") is None:
            raise UnprocessableEntityException(
                {
                    "title": "Project",
                    "message": "Description is required and cannot be empty.",
                }
            )

        for contributor in data.get("contributors", []):
            if not validate_uuid(contributor):
                raise UnprocessableEntityException(
                    {
                        "title": "Project",
                        "status": {
                            "read_only": True,
                        },
                    }
                )
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        print(1111111111111111)
        contributors_data = validated_data.pop("contributors", [])
        project = super().create(validated_data)
        for contributor_id in contributors_data:
            try:
                project.contributors.add(contributor_id)
            except User.DoesNotExist:
                raise UnprocessableEntityException(
                    {
                        "title": "Project",
                        "message": f"User with ID '{contributor_id}' does not exist.",
                    }
                )
        return project


class ProjectEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "contributors",
            "status",
        ]

        extra_kwargs = {
            "id": {
                "read_only": True,
            },
        }

    def is_valid(self, raise_exception=False):
        data = self.initial_data
        if "contributors" in data:
            for contributor in data.get("contributors"):
                if not validate_uuid(contributor):
                    raise UnprocessableEntityException(
                        {
                            "title": "Project",
                            "message": "Invalid contributors",
                        }
                    )
                contributors = User.objects.filter(id=contributor)
                if not contributors.exists():
                    raise UnprocessableEntityException(
                        {
                            "title": "Project",
                            "message": "Contributors do not exist",
                        }
                    )
        return super().is_valid(raise_exception=raise_exception)


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "project",
            "assignee",
            "status",
        ]

        extra_kwargs = {
            "id": {
                "read_only": True,
            },
            "status": {
                "read_only": True,
            },
        }

    def is_valid(self, *, raise_exception=False):
        data = self.initial_data
        if data.get("title") == "" or data.get("title") is None:
            raise UnprocessableEntityException(
                {
                    "title": "Task",
                    "message": "Title is required and cannot be empty.",
                }
            )

        if data.get("description") == "" or data.get("description") is None:
            raise UnprocessableEntityException(
                {
                    "title": "Task",
                    "message": "Description is required and cannot be empty.",
                }
            )

        if not validate_uuid(data.get("project")):
            raise UnprocessableEntityException(
                {
                    "title": "Task",
                    "message": "Invalid project.",
                }
            )

        if not validate_uuid(data.get("assignee")):
            raise UnprocessableEntityException(
                {
                    "title": "Task",
                    "message": "Invalid assignee.",
                }
            )

        project = Project.objects.filter(id=data.get("project"))
        if not project.exists():
            raise UnprocessableEntityException(
                {
                    "title": "Task",
                    "message": "Project does not exist.",
                }
            )

        assignee = User.objects.filter(id=data.get("assignee"))
        if not assignee.exists():
            raise UnprocessableEntityException(
                {
                    "title": "Task",
                    "message": "Assignee does not exist.",
                }
            )

        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        submitter = super().create(validated_data)
        submitter.creator = self.context["request"].user
        submitter.save()
        return submitter


class TaskEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "project",
            "assignee",
            "status",
        ]

        extra_kwargs = {
            "id": {
                "read_only": True,
            },
            "status": {
                "read_only": True,
            },
        }

    def is_valid(self, *, raise_exception=False):
        data = self.initial_data
        if data.get("title") == "" or data.get("title") is None:
            raise UnprocessableEntityException(
                {
                    "title": "Task",
                    "message": "Title is required and cannot be empty.",
                }
            )

        if data.get("description") == "" or data.get("description") is None:
            raise UnprocessableEntityException(
                {
                    "title": "Task",
                    "message": "Description is required and cannot be empty.",
                }
            )

        if not validate_uuid(data.get("project")):
            raise UnprocessableEntityException(
                {
                    "title": "Task",
                    "message": "Invalid project.",
                }
            )

        if not validate_uuid(data.get("assignee")):
            raise UnprocessableEntityException(
                {
                    "title": "Task",
                    "message": "Invalid assignee.",
                }
            )

        project = Project.objects.filter(id=data.get("project"))
        if not project.exists():
            raise UnprocessableEntityException(
                {
                    "title": "Task",
                    "message": "Project does not exist.",
                }
            )

        assignee_qs = User.objects.filter(id=data.get("assignee"))
        if not assignee_qs.exists():
            raise UnprocessableEntityException(
                {
                    "title": "Task",
                    "message": "Assignee does not exist.",
                }
            )
        assignee = assignee_qs.first()
        if not assignee.role == "U":
            raise UnprocessableEntityException(
                {
                    "title": "Task",
                    "message": "Assignee can only be a normal user.",
                }
            )
        return super().is_valid(raise_exception=raise_exception)


class SubmitTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmittedTask
        fields = [
            "id",
            "task",
            "project",
            "remarks",
            "creator",
        ]

        extra_kwargs = {
            "id": {
                "read_only": True,
            },
            "status": {
                "read_only": True,
            },
            "creator": {
                "read_only": True,
            },
        }

    def is_valid(self, *, raise_exception=False):
        data = self.initial_data
        if data.get("task") == "" or data.get("task") is None:
            raise UnprocessableEntityException(
                {
                    "title": "Submit Task",
                    "message": "Task is required and cannot be empty.",
                }
            )

        if not validate_uuid(data.get("task")):
            raise UnprocessableEntityException(
                {
                    "title": "Submit Task",
                    "message": "Invalid task.",
                }
            )

        if data.get("project") == "" or data.get("project") is None:
            raise UnprocessableEntityException(
                {
                    "title": "Submit Task",
                    "message": "Project is required and cannot be empty.",
                }
            )

        if not validate_uuid(data.get("task")):
            raise UnprocessableEntityException(
                {
                    "title": "Submit Task",
                    "message": "Invalid task.",
                }
            )

        task = Task.objects.filter(id=data.get("task"))
        if not task.exists():
            raise UnprocessableEntityException(
                {
                    "title": "Submit Task",
                    "message": "Task does not exist.",
                }
            )

        project = Project.objects.filter(id=data.get("project"))
        if not project.exists():
            raise UnprocessableEntityException(
                {
                    "title": "Submit Task",
                    "message": "Project does not exist.",
                }
            )

        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        submitter = super().create(validated_data)
        submitter.creator = self.context["request"].user
        submitter.save()
        return submitter


class SubmitTaskEditSerializer(serializers.ModelSerializer):
    is_approved = serializers.BooleanField()
    modifier = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = SubmittedTask
        fields = [
            "is_approved",
            "modifier",
        ]

    def update(self, instance, validated_data):
        validated_data["modifier"] = self.context["request"].user
        instance = super().update(instance, validated_data)
        instance.task.status = "O"
        instance.task.save()
        return instance
