from rest_framework.routers import SimpleRouter

from app.api import views

router = SimpleRouter()
router.register("chair", views.ChairViewSet, basename="chair")
router.register("auth", views.AuthViewSet, basename="auth")
router.register("comment", views.CommentViewSet, basename="comment")
