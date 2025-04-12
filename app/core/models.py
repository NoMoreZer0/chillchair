import os
import hashlib

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.functional import cached_property

from app.core.managers import UserManager
from app.shared.utils import get_full_url


class TimestampMixin(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время создания",
        db_index=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Время последнего изменения",
        db_index=True,
    )


class User(AbstractUser, TimestampMixin):
    objects = UserManager()
    email = models.EmailField(name="email", unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # No extra required fields

    def __str__(self):
        return self.email


class Chair(TimestampMixin):
    def _upload_path(self, filename):
        _, file_name = os.path.split(self.thumbnail.name)
        file_root, file_ext = os.path.splitext(file_name)
        return f"chair_thumbnails/{self.id}/{file_root}.{self.image_hash()}{file_ext}"

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=False)
    specs = models.JSONField(blank=True, null=True)
    location = models.CharField(blank=True, null=True)
    thumbnail = models.ImageField(blank=True, null=True, upload_to=_upload_path)

    class Status(models.TextChoices):
        draft = "draft"
        review = "review"
        published = "published"

    status = models.CharField(
        choices=Status.choices, default=Status.draft, max_length=10
    )

    def image_hash(self):
        """
        Return a hash of the file with the given name and optional content.
        """
        sha256 = hashlib.sha256()
        for chunk in self.thumbnail.chunks():
            sha256.update(chunk)
        self.thumbnail.seek(0)
        return sha256.hexdigest()[:12]

    @property
    def get_thumbnail(self):
        return get_full_url(self.thumbnail) if self.thumbnail else None


class ChairImage(TimestampMixin):
    def _upload_path(self, filename):
        _, file_name = os.path.split(self.image.name)
        file_root, file_ext = os.path.splitext(file_name)
        return f"chair_images/{self.id}/{file_root}.{self.image_hash()}{file_ext}"

    chair = models.ForeignKey(Chair, on_delete=models.CASCADE)
    image = models.ImageField()

    def image_hash(self):
        """
        Return a hash of the file with the given name and optional content.
        """
        sha256 = hashlib.sha256()
        for chunk in self.image.chunks():
            sha256.update(chunk)
        self.image.seek(0)
        return sha256.hexdigest()[:12]


class Rating(TimestampMixin):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.FloatField(default=0)

    class Source(models.TextChoices):
        Chair = "Chair"

    SOURCE_DICT = {
        "Chair": Chair,
    }

    source = models.CharField(choices=Source.choices, db_index=True, max_length=50)
    source_id = models.BigIntegerField(db_index=True)

    @cached_property
    def source_object(self):
        return self.SOURCE_DICT[self.source].objects.get(pk=self.source_id)


class Comment(TimestampMixin):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()

    class Source(models.TextChoices):
        Chair = "Chair"

    SOURCE_DICT = {
        "Chair": Chair,
    }

    source = models.CharField(choices=Source.choices, db_index=True, max_length=50)
    source_id = models.BigIntegerField(db_index=True)

    @cached_property
    def source_object(self):
        return self.SOURCE_DICT[self.source].objects.get(pk=self.source_id)
