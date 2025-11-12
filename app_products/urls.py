from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet

class OptionalSlashRouter(DefaultRouter):
    trailing_slash = '/?'

router = OptionalSlashRouter()
router.register(r"products", ProductViewSet, basename="product")

urlpatterns = [
    path("", include(router.urls)),
]