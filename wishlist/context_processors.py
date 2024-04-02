from .models import Wishlist
from product.models import Product

from django.shortcuts import get_object_or_404
from decimal import Decimal


def wishlists_count(request):
    wishlist_items = None
    wishlist_items_count = 0
    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user)
        wishlist_items_count = wishlist_items.count()

    return {'wishlist_items_count': wishlist_items_count}


def wishlists_items(request):
    wishlist_items = None

    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user)

    return {'wishlist_items': wishlist_items}
