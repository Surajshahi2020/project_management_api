from rest_framework import serializers

from assigner.models import User
from common.exceptions import UnprocessableEntityException
from common.utils import (
    validate_email,
    validate_password,
    validate_phone,
    validate_url,
)


class AccountsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "full_name",
            "phone",
            "email",
            "gender",
            "date_of_birth",
            "profile_pic",
            "password",
        ]

        extra_kwargs = {
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
