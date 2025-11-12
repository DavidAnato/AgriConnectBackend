from rest_framework import serializers
from .models import Product, ProductMedia
from app_authentication.serializers import UserProfileSerializer

class ProductMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMedia
        fields = ["id", "media_type", "file", "created_at"]

class ProductSerializer(serializers.ModelSerializer):
    medias = ProductMediaSerializer(many=True, read_only=True)
    producer = UserProfileSerializer(read_only=True)

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
            "producer",
            "producer",
            "is_published",
            "created_at",
            "updated_at",
            "medias",
        ]
        read_only_fields = ["producer"]