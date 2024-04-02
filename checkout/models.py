from django.db import models
from django.utils import timezone
from django_countries.fields import CountryField
from babel.numbers import format_currency
import uuid

from product.models import Product
# Create your models here.


class Order(models.Model):
    order_number = models.CharField(max_length=254,  blank=True)
    user_id = models.CharField(max_length=254, null=True)
    email = models.EmailField(null=False)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    phone = models.TextField(max_length=20)
    street_address = models.TextField(max_length=250)
    post_code = models.TextField(max_length=20, blank=True)
    city = models.TextField(max_length=80)
    state = models.TextField(max_length=80, default="")
    country = models.CharField(max_length=200,  null=True, choices=CountryField(
    ).choices + [('', 'Select Country')])
    status = models.CharField(max_length=50, blank=True, default="In-Progress")
    shipping_method = models.TextField(max_length=80, default="")
    shipping_price = models.DecimalField(max_digits=6, decimal_places=2)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_pid = models.CharField(max_length=254,  blank=True)
    lineitem = models.ManyToManyField(
        'OrderLineItem', related_name='orders', blank=True)
    created_at = models.DateTimeField(default=timezone.now, blank=True)

    def formatted_sub_total(self):
        return format_currency(self.sub_total, 'EUR', locale='en_US')

    def formatted_grand_total(self):
        return format_currency(self.grand_total, 'EUR', locale='en_US')

    def formatted_shipping_price(self):
        return format_currency(self.shipping_price, 'EUR', locale='en_US')

    def _generate_order_number(self):
        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'order by {self.first_name} {self.last_name}'


class OrderLineItem(models.Model):
    order = models.ForeignKey(
        Order, blank=True, on_delete=models.CASCADE,  related_name='lineitems')
    product = models.ForeignKey(
        Product, blank=True, null=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField(blank=True)
    line_item_total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now, blank=True)

    def save(self, *args, **kwargs):
        self.line_item_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "OrderLineItems"

    def __str__(self):
        return f'order items for {self.order.order_number}'
