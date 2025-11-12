from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Sum, Count, F
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from app_products.models import Product
from .models import Cart, CartItem, Order, OrderItem
from .serializers import (
    CartSerializer, AddCartItemSerializer, RemoveCartItemSerializer,
    OrderSerializer,
)


class CartViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def _get_or_create_cart(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return cart

    def list(self, request):
        cart = self._get_or_create_cart(request)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=["post"], url_path="add-item")
    def add_item(self, request):
        cart = self._get_or_create_cart(request)
        serializer = AddCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_id = serializer.validated_data["product_id"]
        quantity = serializer.validated_data["quantity"]

        product = get_object_or_404(Product, id=product_id, is_published=True)

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={"quantity": quantity, "unit_price": product.unit_price},
        )
        if not created:
            item.quantity = quantity
            item.unit_price = product.unit_price
            item.save()

        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="remove-item")
    def remove_item(self, request):
        cart = self._get_or_create_cart(request)
        serializer = RemoveCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item_id = serializer.validated_data["item_id"]

        item = get_object_or_404(CartItem, id=item_id, cart=cart)
        item.delete()
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="clear")
    def clear(self, request):
        cart = self._get_or_create_cart(request)
        cart.items.all().delete()
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="checkout")
    def checkout(self, request):
        cart = self._get_or_create_cart(request)
        if cart.items.count() == 0:
            return Response({"detail": "Le panier est vide."}, status=status.HTTP_400_BAD_REQUEST)
        shipping_address = request.data.get("shipping_address", "")
        # Regrouper les items par producteur
        items_by_producer = {}
        for item in cart.items.select_related("product", "product__producer"):
            producer = item.product.producer
            items_by_producer.setdefault(producer, []).append(item)

        created_orders = []
        for producer, items in items_by_producer.items():
            order = Order.objects.create(
                user=request.user,
                producer=producer,
                shipping_address=shipping_address,
            )
            total = 0
            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    product_name=item.product.name,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                )
                total += item.quantity * item.unit_price
            order.total = total
            order.save()
            created_orders.append(order)

        # Vider le panier après commande
        cart.items.all().delete()

        return Response(OrderSerializer(created_orders, many=True).data, status=status.HTTP_201_CREATED)


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by("-created_at")

    @action(detail=False, methods=["get"], url_path="vendor")
    def vendor_orders(self, request):
        # Liste des commandes pour le producteur connecté
        qs = Order.objects.filter(producer=request.user).order_by("-created_at")
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = OrderSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = OrderSerializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="vendor-stats")
    def vendor_stats(self, request):
        # Statistiques de dashboard pour le producteur connecté
        user = request.user

        # Période optionnelle ?start=YYYY-MM-DD&end=YYYY-MM-DD
        start_str = request.query_params.get("start")
        end_str = request.query_params.get("end")
        order_filter = {"producer": user}
        if start_str:
            try:
                start = timezone.datetime.fromisoformat(start_str)
                order_filter["created_at__gte"] = start
            except Exception:
                pass
        if end_str:
            try:
                # inclure la fin de journée
                end = timezone.datetime.fromisoformat(end_str)
                if end.tzinfo is None:
                    end = timezone.make_aware(end)
                end = end.replace(hour=23, minute=59, second=59)
                order_filter["created_at__lte"] = end
            except Exception:
                pass

        orders_qs = Order.objects.filter(**order_filter)
        total_orders = orders_qs.count()
        by_status = {
            "pending": orders_qs.filter(status="pending").count(),
            "paid": orders_qs.filter(status="paid").count(),
            "shipped": orders_qs.filter(status="shipped").count(),
            "completed": orders_qs.filter(status="completed").count(),
            "cancelled": orders_qs.filter(status="cancelled").count(),
        }

        revenue_qs = orders_qs.filter(status__in=["paid", "completed"]).aggregate(total_revenue=Sum("total"))
        total_revenue = revenue_qs.get("total_revenue") or 0

        items_qs = OrderItem.objects.filter(order__in=orders_qs.filter(status__in=["paid", "completed"]))
        items_sold = items_qs.aggregate(qty=Sum("quantity")).get("qty") or 0

        top_products = (
            items_qs.values("product_name")
            .annotate(
                quantity_sold=Sum("quantity"),
                revenue=Sum(F("quantity") * F("unit_price")),
            )
            .order_by("-quantity_sold")[:5]
        )

        data = {
            "totals": {
                "orders": total_orders,
                "revenue": total_revenue,
                "items_sold": items_sold,
            },
            "by_status": by_status,
            "top_products": list(top_products),
            "period": {
                "start": start_str,
                "end": end_str,
            },
        }

        return Response(data)