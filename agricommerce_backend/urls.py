from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="AgriCommerce API",
        default_version="v1",
        description="Documentation de l'API pour l'application AgriCommerce",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@agricommerce.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("authentication/", include("app_authentication.urls")),
    path("products/", include("app_products.urls")),
    path("commerce/", include("app_commerce.urls")),

    # 🔍 Swagger & Redoc endpoints
    path("swagger/", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path("redoc/", schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path("swagger.json", schema_view.without_ui(cache_timeout=0), name='schema-json'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)