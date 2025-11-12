from django.contrib import admin
from .models import Product, ProductMedia, Category

class ProductMediaInline(admin.TabularInline):
    model = ProductMedia
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "unit_type", "unit_price", "quantity_available", "producer", "is_published", "created_at")
    search_fields = ("name", "producer__email", "location_village", "location_commune", "category__name")
    list_filter = ("unit_type", "is_published", "category")
    inlines = [ProductMediaInline]

@admin.register(ProductMedia)
class ProductMediaAdmin(admin.ModelAdmin):
    list_display = ("product", "media_type", "created_at")
    list_filter = ("media_type",)
    

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)
    