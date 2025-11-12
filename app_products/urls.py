from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryViewSet

class OptionalSlashRouter(DefaultRouter):
    trailing_slash = '/?'

router = OptionalSlashRouter()
router.register(r"products", ProductViewSet, basename="product")
router.register(r"categories", CategoryViewSet, basename="category")

urlpatterns = [
    path("", include(router.urls)),
]