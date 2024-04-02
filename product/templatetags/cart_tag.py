from django import template

register = template.Library()

@register.filter
def is_in_cart(product, carts):
    cart_item = next((item for item in carts if item['product_id'] == str(product.id)), None)
    if cart_item:                    
        return True
    else:
        return False
