from .models import Category, Product
from django.shortcuts import get_object_or_404


def categories(request):
    categories = Category.objects.all()
    return {"categories": categories}


def featured_product(request):
    featured_product = Product.objects.filter(is_featured=True)
    return {"featured_product": featured_product}
