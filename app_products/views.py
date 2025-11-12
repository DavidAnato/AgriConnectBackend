from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Product
from .serializers import ProductSerializer

class IsProducerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.producer == request.user or getattr(request.user, "is_staff", False)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["unit_type", "is_published", "location_commune", "location_village", "producer"]
    search_fields = ["name", "short_description", "long_description", "location_village", "location_commune"]
    ordering_fields = ["created_at", "updated_at", "unit_price", "quantity_available", "name"]
    ordering = ["-created_at"]

    def perform_create(self, serializer):
        if not self.request.user or not self.request.user.is_authenticated:
            raise ValidationError({"detail": "Authentification requise"})
        serializer.save(producer=self.request.user)

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        elif self.action == "create":
            return [permissions.IsAuthenticated()]
        elif self.action in ["update", "partial_update", "destroy"]:
            return [permissions.IsAuthenticated(), IsProducerOrAdmin()]
        return super().get_permissions()

    @action(detail=False, methods=["get"], url_path=r"producer/(?P<producer_id>\d+)", permission_classes=[permissions.AllowAny])
    def list_by_producer(self, request, producer_id=None):
        """Liste les produits d'un producteur spécifié.

        - Public: ne retourne que les produits publiés.
        - Producteur lui-même ou admin: peut inclure les non publiés avec `include_unpublished=true`.
        """
        include_unpublished = request.query_params.get("include_unpublished") == "true"
        queryset = Product.objects.filter(producer_id=producer_id)

        # Restreindre aux publiés pour le public
        if not (request.user.is_authenticated and (request.user.is_staff or request.user.id == int(producer_id))):
            queryset = queryset.filter(is_published=True)
        elif not include_unpublished:
            queryset = queryset.filter(is_published=True)

        # Appliquer filtres/tri/recherche existants
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)