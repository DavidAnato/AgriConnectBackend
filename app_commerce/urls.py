from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CartViewSet, OrderViewSet

class OptionalSlashRouter(DefaultRouter):
    trailing_slash = '/?'

router = OptionalSlashRouter()
router.register(r"cart", CartViewSet, basename="cart")
router.register(r"orders", OrderViewSet, basename="order")

urlpatterns = [
    path("", include(router.urls)),
]