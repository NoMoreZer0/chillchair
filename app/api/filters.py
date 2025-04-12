from django_filters.rest_framework import FilterSet

from app.core import models as core_models

class CommentFilter(FilterSet):
    class Meta:
        model = core_models.Comment
        fields = [
            "source",
            "source_id"
        ]