from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ["id", "product", "product_name", "quantity", "unit_price", "subtotal", "created_at", "updated_at"]

    def get_subtotal(self, obj):
        return obj.subtotal


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "user", "items", "total", "created_at", "updated_at"]
        read_only_fields = ["user"]

    def get_total(self, obj):
        return obj.total


class AddCartItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.DecimalField(max_digits=12, decimal_places=2)


class RemoveCartItemSerializer(serializers.Serializer):
    item_id = serializers.IntegerField()


class OrderItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ["id", "product", "product_name", "quantity", "unit_price", "subtotal"]

    def get_subtotal(self, obj):
        return obj.quantity * obj.unit_price


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    producer = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "producer",
            "status",
            "total",
            "shipping_address",
            "created_at",
            "updated_at",
            "items",
        ]
        read_only_fields = ["user", "producer", "total"]