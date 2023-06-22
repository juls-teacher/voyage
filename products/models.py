from django.db import models
from django.conf import settings
from decimal import Decimal


class Product(models.Model):

    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    price = models.DecimalField(default=Decimal("0"), decimal_places=5, max_digits=10)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"Product : {self.title} - {self.price}"