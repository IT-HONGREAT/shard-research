from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from app.user.models import User
from app.user.v1.filters import UserFilter
from app.user.v1.serializers import UserLoginSerializer, UserRegisterSerializer, UserSerializer


@extend_schema_view(
    list=extend_schema(summary="유저 목록 조회"),
    me=extend_schema(summary="유저 조회"),
    login=extend_schema(summary="유저 로그인"),
    refresh=extend_schema(summary="유저 리프레시"),
    register=extend_schema(summary="유저 생성"),
)
class UserViewSet(
    mixins.ListModelMixin,
    GenericViewSet,
):

    queryset = User.objects.all()
    filter_class = UserFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        location_params = self.request.GET.get("location")
        database_mapper = {
            "KO": "shard_1",
            "US": "shard_2",
        }
        using_db = database_mapper.get(location_params, "default")
        return queryset.using(using_db)

    def get_serializer_class(self):
        if self.action == "list":
            return UserSerializer
        if self.action == "me":
            return UserSerializer
        if self.action == "login":
            return UserLoginSerializer
        if self.action == "refresh":
            return TokenRefreshSerializer
        if self.action == "register":
            return UserRegisterSerializer

        raise Exception

    def get_permissions(self):
        if self.action == "me":
            return [IsAuthenticated()]
        return []

    def _create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=["GET"], detail=False)
    def me(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.request.user)
        return Response(serializer.data)

    @action(methods=["POST"], detail=False)
    def login(self, request, *args, **kwargs):
        return self._create(request, *args, **kwargs)

    @action(methods=["POST"], detail=False)
    def refresh(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=False)
    def register(self, request, *args, **kwargs):

        return self._create(request, *args, **kwargs)
