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
            "status",
            "thumbnail",
            "location",
            "specs",
            "is_author",
            "longitude",
            "latitude",
            "city",
            "road",
            "status",
        )

    thumbnail = serializers.CharField(source="get_thumbnail")
    is_author = serializers.SerializerMethodField()

    def get_is_author(self, obj):
        return obj.author == self.context["request"].user

class ChairUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.Chair
        fields = (
            "title",
            "description",
            "thumbnail",
            "location",
            "specs",
            "longitude",
            "latitude",
            "city",
            "road",
            "status",
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
            "longitude",
            "latitude",
            "city",
            "road",
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
    groups = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )

    class Meta:
        model = core_models.User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "groups",
        )

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.User
        fields = (
            "first_name",
            "last_name",
        )

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    def validate(self, data):
        data["email"] = data["email"].lower()
        if core_models.User.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError(
                {"email": f'{data["email"]} already exists'}
            )
        return data

    def create(self, validated_data):
        user = core_models.User.objects.create_user(
            email=validated_data["email"], password=validated_data["password"]
        )
        return user


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.Comment
        fields = ("id", "source", "source_id", "message", "author")

    author = UserSerializer(read_only=True)


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.Comment
        fields = ("source", "source_id", "message")

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        comment = core_models.Comment.objects.create(**validated_data)
        return comment


class RatingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.Rating
        fields = ("source", "source_id", "rating")

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        rating = core_models.Rating.objects.create(**validated_data)
        return rating


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.Rating
        fields = ("id", "source", "source_id", "rating")
