import os
import hashlib

from django.contrib.auth.models import AbstractUser
from django.db import models

from app.core.managers import UserManager


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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # No extra required fields

    def __str__(self):
        return self.email


class Chair(TimestampMixin):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=False)
    specs = models.JSONField(blank=True, null=True)
    location = models.CharField(blank=True, null=True)

    class Status(models.TextChoices):
        draft = "draft"
        review = "review"
        published = "published"

    status = models.CharField(choices=Status.choices, default=Status.draft, max_length=10)

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
