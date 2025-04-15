from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import JSONField
from django_json_widget.widgets import JSONEditorWidget

from app.core.models import User, Chair, ChairImage, Rating, Comment


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("id", "email", "first_name", "last_name")


class ChairImageInline(admin.StackedInline):
    model = ChairImage
    extra = 0


@admin.register(ChairImage)
class ChairImageAdmin(admin.ModelAdmin):
    list_display = ("id", "chair", "image")
    raw_id_fields = ("chair",)
    list_filter = ("chair",)


@admin.register(Chair)
class Chair(admin.ModelAdmin):
    list_display = ("id", "title", "author", "status", "city", "created_at", "updated_at")
    inlines = (ChairImageInline,)
    raw_id_fields = ("author",)
    formfield_overrides = {
        JSONField: {"widget": JSONEditorWidget},
    }
    list_filter = ("status",)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "source", "source_id", "rating")
    raw_id_fields = ("author",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "source", "source_id", "message")
    raw_id_fields = ("author",)
