from django.contrib.auth import get_user_model
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.viewsets import mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from app.api import serializers
from app.api import filters
from app.core import models as core_models


class ChairViewSet(viewsets.ModelViewSet):
    queryset = core_models.Chair.objects.all()
    serializer_classes = {
        "list": serializers.ChairSerializer,
        "retrieve": serializers.ChairSerializer,
        "create": serializers.ChairCreateSerializer,
        "update": serializers.ChairUpdateSerializer,
        "partial_update": serializers.ChairUpdateSerializer,
        "upload_thumbnail": serializers.ThumbnailUploadSerializer,
        "my": serializers.ChairSerializer,
    }
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        return self.serializer_classes[self.action]

    def get_permissions(self):
        if action in ["list", "retrieve"]:
            return [p() for p in [AllowAny]]
        return [p() for p in self.permission_classes]

    @action(detail=True, methods=["post"], url_path="upload-thumbnail")
    def upload_thumbnail(self, request, pk=None):
        chair = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        chair.thumbnail = serializer.validated_data["thumbnail"]
        chair.save()

        response_serializer = serializers.ChairSerializer(
            chair, context={"request": request}
        )
        return Response(response_serializer.data)

    @action(detail=False, methods=["get"])
    def my(self, request, pk=None):
        queryset = self.get_queryset().filter(author=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def submit(self, request, pk=None):
        chair = self.get_object()
        if chair.status != core_models.Chair.Status.draft or chair.author != request.user:
            return Response({"error": "You can't submit this chair"})
        chair.status = core_models.Chair.Status.review
        chair.save()
        return Response(serializers.ChairSerializer(chair, context={"request": request}).data)


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_classes = {
        "login": serializers.LoginSerializer,
        "register": serializers.RegisterSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes[self.action]

    @action(methods=["post"], detail=False)
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.create(serializer.validated_data))

    @action(methods=["post"], detail=False)
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.create(serializer.validated_data)
        return Response(serializers.UserSerializer(user).data)


class ChairImageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = core_models.ChairImage.objects.all()


class CommentViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = core_models.Comment.objects.all()
    serializer_classes = {
        "create": serializers.CommentCreateSerializer,
        "list": serializers.CommentSerializer,
    }
    filterset_class = filters.CommentFilter
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        return self.serializer_classes[self.action]

    def get_permissions(self):
        if action in ["list"]:
            return [p() for p in [AllowAny]]
        return [p() for p in self.permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = serializer.create(serializer.validated_data)
        return Response(serializers.CommentSerializer(comment).data)


class RatingViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = core_models.Rating.objects.all()
    serializer_classes = {
        "list": serializers.RatingSerializer,
        "create": serializers.RatingCreateSerializer,
    }
    filterset_class = filters.RatingFilter
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        return self.serializer_classes[self.action]

    def get_permissions(self):
        if action in ["list"]:
            return [p() for p in [AllowAny]]
        return [p() for p in self.permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rating = serializer.create(serializer.validated_data)
        return Response(serializers.RatingCreateSerializer(rating).data)

class UserViewSet(viewsets.GenericViewSet):
    queryset = get_user_model().objects.all()
    serializer_classes = {
        "profile": serializers.UserSerializer,
        "profile_update": serializers.UserUpdateSerializer,
    }
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        return self.serializer_classes[self.action]


    @action(detail=False, methods=["get"])
    def profile(self, request, pk=None):
        serializer = self.get_serializer(instance=request.user)
        return Response(serializer.data)

    @action(detail=False, methods=["put"])
    def profile_update(self, request, pk=None):
        serializer = self.get_serializer(instance=request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializers.UserSerializer(user).data)


def status(request):
    # DB Health check
    get_user_model().objects.exists()
    return HttpResponse("")
