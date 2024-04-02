from django.db import models
from django.utils import timezone

from user.models import CustomUser
from product.models import Product
# Create your models here.


class Cart(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='carts')
    quantity = models.IntegerField(blank=True, default=1)
    created_at = models.DateTimeField(default=timezone.now, blank=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"Carts Item for {self.user.email}"
