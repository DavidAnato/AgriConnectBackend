from django.contrib import admin
from .models import Product, ProductMedia

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "unit_type", "unit_price", "quantity_available", "producer", "is_published", "created_at")
    search_fields = ("name", "producer__email", "location_village", "location_commune")
    list_filter = ("unit_type", "is_published")

@admin.register(ProductMedia)
class ProductMediaAdmin(admin.ModelAdmin):
    list_display = ("product", "media_type", "created_at")
    list_filter = ("media_type",)