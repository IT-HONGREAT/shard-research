from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from app.user.models import User
from app.user.v1.examples import login_examples


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
        ]


@extend_schema_serializer(examples=login_examples)
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        self.user = authenticate(
            request=self.context["request"],
            email=attrs["email"],
            password=attrs["password"],
        )
        if self.user:
            refresh = self.get_token(self.user)
        else:
            raise ValidationError(
                {
                    "email": ["인증정보가 일치하지 않습니다."],
                    "password": ["인증정보가 일치하지 않습니다."],
                }
            )

        data = dict()
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        if attrs.get("device"):
            self.user.connect_device(**attrs["device"])

        return data

    def create(self, validated_data):
        return validated_data


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email"]


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "location",
        ]
