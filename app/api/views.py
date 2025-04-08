from django.contrib.auth import get_user_model
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from app.api import serializers
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
    }
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        return self.serializer_classes[self.action]

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


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_classes = {
        "login": serializers.LoginSerializer,
        "register": serializers.RegisterSerializer
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


def status(request):
    # DB Health check
    get_user_model().objects.exists()
    return HttpResponse("")
