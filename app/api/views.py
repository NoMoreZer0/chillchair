from django.contrib.auth import get_user_model
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from app.api import serializers
from app.api import filters
from app.api import permissions
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
    filterset_class = filters.ChairFilter

    def get_serializer_class(self):
        return self.serializer_classes[self.action]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [p() for p in [AllowAny]]
        if self.action in ["publish", "reject", "statistics"]:
            return [p() for p in [permissions.ModeratorPermission]]
        return [p() for p in self.permission_classes]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

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
            raise ValidationError("You are not authorized to submit this chair")
        chair.status = core_models.Chair.Status.review
        chair.save()
        return Response(serializers.ChairSerializer(chair, context={"request": request}).data)

    @action(detail=True, methods=["post"])
    def publish(self, request, pk):
        chair = self.get_object()
        if chair.status != core_models.Chair.Status.review:
            raise ValidationError("You can't publish this chair")
        chair.status = core_models.Chair.Status.published
        chair.save()
        return Response(serializers.ChairSerializer(chair, context={"request": request}).data)

    @action(detail=True, methods=["post"])
    def reject(self, request, pk):
        chair = self.get_object()
        if chair.status != core_models.Chair.Status.review:
            raise ValidationError("You can't reject this chair")
        chair.status = core_models.Chair.Status.rejected
        chair.save()
        return Response(serializers.ChairSerializer(chair, context={"request": request}).data)

    @action(detail=False, methods=["get"])
    def statistics(self, request):
        all_chairs_count = self.get_queryset().count()
        rejected_chairs_count = self.get_queryset().filter(status=core_models.Chair.Status.rejected).count()
        published_chairs_count = self.get_queryset().filter(status=core_models.Chair.Status.published).count()
        draft_chairs_count = self.get_queryset().filter(status=core_models.Chair.Status.draft).count()
        return Response({
            "all_chairs_count": all_chairs_count,
            "rejected_chairs_count": rejected_chairs_count,
            "published_chairs_count": published_chairs_count,
            "draft_chairs_count": draft_chairs_count,
        })


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

    def get_permissions(self,):
        if self.action in ["list"]:
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
