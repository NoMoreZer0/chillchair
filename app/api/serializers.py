from rest_framework import serializers
from rest_framework.authtoken.models import Token

from app.core import models as core_models


class ChairSerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.Chair
        fields = (
            "id",
            "title",
            "description",
            "thumbnail",
            "location",
            "specs",
        )

    thumbnail = serializers.CharField(source="get_thumbnail")


class ChairUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.Chair
        fields = (
            "title",
            "description",
            "thumbnail",
            "location",
            "specs",
        )


class ChairCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.Chair
        fields = (
            "title",
            "description",
            "thumbnail",
            "location",
            "specs",
        )

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        chair = core_models.Chair.objects.create(**validated_data)
        return chair

class ThumbnailUploadSerializer(serializers.Serializer):
    thumbnail = serializers.ImageField()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        data["email"] = data["email"].lower()
        try:
            data["user"] = core_models.User.objects.get(email=data["email"])
        except core_models.User.DoesNotExist:
            raise serializers.ValidationError(
                {"email": f'{data["email"]} does not exists'}
            )
        if not data["user"].check_password(data["password"]):
            raise serializers.ValidationError({"password": "Password is incorrect"})
        return data

    def create(self, validated_data):
        Token.objects.filter(user=validated_data["user"]).delete()
        token = Token.objects.create(user=validated_data["user"])
        return {"token": token.key}

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
        )

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )

    def validate(self, data):
        data["email"] = data["email"].lower()
        if core_models.User.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError(
                {"email": f'{data["email"]} already exists'}
            )
        return data

    def create(self, validated_data):
        user = core_models.User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"]
        )
        return user
