import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from django.template import loader
from django.utils import timezone
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from app.user.models import User
from app.user.social_adapters import SocialAdapter
from app.user.v1.examples import login_examples
from app.user.validators import validate_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "phone"]




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

