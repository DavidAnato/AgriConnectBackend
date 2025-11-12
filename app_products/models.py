from django.db import models
from django.conf import settings

class Product(models.Model):
    UNIT_CHOICES = (
        ("unit", "Par unité"),
        ("kg", "Au kilo"),
    )

    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="products/main/", null=True, blank=True)
    short_description = models.CharField(max_length=300, blank=True)
    long_description = models.TextField(blank=True)
    unit_type = models.CharField(max_length=10, choices=UNIT_CHOICES, default="unit")
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity_available = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    location_village = models.CharField(max_length=255, blank=True)
    location_commune = models.CharField(max_length=255, blank=True)
    producer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="products")
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Produit"
        verbose_name_plural = "Produits"

    def __str__(self):
        return self.name

class ProductMedia(models.Model):
    MEDIA_TYPE_CHOICES = (
        ("image", "Image"),
        ("video", "Vidéo"),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="medias")
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default="image")
    file = models.FileField(upload_to="products/medias/")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Média du produit"
        verbose_name_plural = "Médias du produit"

    def __str__(self):
        return f"{self.media_type} - {self.product.name}"