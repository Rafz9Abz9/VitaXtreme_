from django.db import models
from django.core.validators import validate_image_file_extension, MinValueValidator, MaxValueValidator
from .utils import validate_image_content
from babel.numbers import format_currency
from django.utils import timezone
from django_currentuser.middleware import (get_current_authenticated_user)

from user.models import CustomUser


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=25, null=False)
    friendly_name = models.CharField(max_length=50, null=False, default=" ")

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Image(models.Model):
    # Fields to store information about each image
    image_file = models.ImageField(
        upload_to='product_images/',
        validators=[validate_image_file_extension, validate_image_content],
        default="images/products/default.jpeg"
    )
    caption = models.CharField(max_length=255, blank=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


class Review(models.Model):
    # Fields to store information about each image
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255, default="")
    content = models.TextField(max_length=1025)
    ratings = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=0
    )
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, related_name='reviews')
    created_at = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return f"Review for {self.product.name}"


class Product(models.Model):
    category = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    ingredients = models.TextField(null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.BigIntegerField(default=0, null=False)
    sold = models.BigIntegerField(default=0, null=False)
    is_featured = models.BooleanField(default=False)
    images = models.ManyToManyField(
        'Image', related_name='products', blank=True)
    ratings = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=0
    )
    review = models.ManyToManyField(
        'Review', related_name='products', blank=True)
    created_at = models.DateTimeField(default=timezone.now, blank=True)

    def formatted_price(self):
        return format_currency(self.price, 'EUR', locale='en_US')

    def is_in_wishlist(self):
        # Access request user using threading
        from wishlist.models import Wishlist

        user = get_current_authenticated_user()

        if user:
            return Wishlist.objects.filter(user=user, product=self).exists()

    def is_in_cart(self):
        # Access request user using threading
        from cart.models import Cart

        user = get_current_authenticated_user()

        if user:
            return Cart.objects.filter(user=user, product=self).exists()

    def __str__(self):
        return self.name
