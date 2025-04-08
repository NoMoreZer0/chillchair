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

