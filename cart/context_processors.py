from .models import Cart
from product.models import Product

from django.shortcuts import get_object_or_404
from decimal import Decimal
from babel.numbers import format_currency
from django.conf import settings


def cart_count(request):
    cart_items = None
    cart_items_count = 0
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        cart_items_count = cart_items.count()
    else:
        carts = request.session.get('carts', [])

        if not carts:
            return {'cart_itmes_count': 0}

        cart_item = []
        for item in carts:
            if isinstance(item, dict) and 'product_id' in item and 'quantity' in item:
                product = get_object_or_404(Product, pk=item['product_id'])
                cart_item.append(
                    {'product': product, 'quantity': item['quantity']})
                cart_items_count = len(cart_item)

    return {'cart_itmes_count': cart_items_count}


def cart_item(request):
    full_cart_item = None
    cart_item = None
    summed_price = 0
    SHIPPING_METHOD_STANDARD = settings.SHIPPING_METHOD_STANDARD
    SHIPPING_METHOD_EXPRESS = settings.SHIPPING_METHOD_EXPRESS
    formatted_sub_total_price = format_currency(0, 'EUR', locale='en_US')

    if request.user.is_authenticated:
        full_cart_item = (Cart.objects.filter(
            user=request.user).order_by('-created_at'))
        cart_item = (Cart.objects.filter(
            user=request.user).order_by('-created_at')[:2])
        # Calculate total price
        summed_price = sum(
            item.quantity * item.product.price for item in full_cart_item)
        formatted_sub_total_price = format_currency(
            summed_price, 'EUR', locale='en_US')

    else:
        carts = request.session.get('carts', [])

        if not carts:
            return {'cart_item': []}

        cart_item = []
        for item in carts:
            if isinstance(item, dict) and 'product_id' in item and 'quantity' in item:
                product = get_object_or_404(Product, pk=item['product_id'])
                cart_item.append(
                    {'product': product, 'quantity': item['quantity']})
                summed_price += Decimal(item['quantity']) * \
                    Decimal(product.price)
                formatted_sub_total_price = format_currency(
                    summed_price, 'EUR', locale='en_US')
        full_cart_item = cart_item
        cart_item = cart_item[:2]

    return {
        'reduced_cart_item': cart_item,
        'full_cart_item': full_cart_item,
        'cart_item_sub_total_price': summed_price,
        'formatted_sub_total_price': formatted_sub_total_price,
        'shipping_express': SHIPPING_METHOD_EXPRESS,
        'formatted_shipping_express': format_currency(SHIPPING_METHOD_EXPRESS, 'EUR', locale='en_US'),
        'shipping_standard': SHIPPING_METHOD_STANDARD,
        'formatted_shipping_standard': format_currency(SHIPPING_METHOD_STANDARD, 'EUR', locale='en_US'),
        'formatted_shipping_standard': format_currency(SHIPPING_METHOD_STANDARD, 'EUR', locale='en_US'),

    }
