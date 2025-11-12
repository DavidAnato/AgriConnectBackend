from rest_framework import serializers
from .models import Product, ProductMedia, Category
from app_authentication.serializers import UserProfileSerializer

class ProductMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMedia
        fields = ["id", "media_type", "file", "created_at"]

class ProductSerializer(serializers.ModelSerializer):
    medias = ProductMediaSerializer(many=True, read_only=True)
    producer = UserProfileSerializer(read_only=True)
    category = serializers.SerializerMethodField(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source="category", write_only=True, required=False)

    def get_category(self, obj):
        if obj.category:
            return {"id": obj.category.id, "name": obj.category.name}
        return None

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "image",
            "short_description",
            "long_description",
            "unit_type",
            "unit_price",
            "quantity_available",
            "location_village",
            "location_commune",
            "category",
            "category_id",
            "producer",
            "producer",
            "is_published",
            "created_at",
            "updated_at",
            "medias",
        ]
        read_only_fields = ["producer"]


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Category
        fields = ["id", "name", "created_at", "product_count"]