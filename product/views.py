from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.functions import Lower
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.db.models import Q

from .models import Product, Category, Review

# Create your views here.


def products(request):
    products = Product.objects.all().order_by('-created_at')
    sort = None
    direction = None
    query = ''
    if request.GET:
        category_name = request.GET.get('category')

        if 'q' in request.GET:
            query = request.GET['q']

            if not query:
                messages.error(
                    request, 'You didn\'t enter any search criteria')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            queries = Q(name__icontains=query) | Q(
                description__icontains=query)
            products = products.filter(queries)

        if category_name:
            category = get_object_or_404(Category, name=category_name)
            products = Product.objects.filter(
                category=category
            )

        if 'sort' in request.GET:
            sortKey = request.GET['sort']
            sort = sortKey

            if sortKey == 'name':
                sortKey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))

            if sortKey == 'date':
                sortKey = 'created_at'

            if 'direction' in request.GET:
                direction = request.GET['direction']
                sort = f'{sort}_{direction}'
                if direction == 'dsc':
                    sortKey = f'-{sortKey}'
            products = products.order_by(sortKey)

    paginator = Paginator(products, 10)
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'current_sorting': sort,
        'products': products,
        'search_term': query
    }
    return render(request, 'products/products.html', context)


def product_details(request, product_id):

    product = get_object_or_404(Product,  pk=product_id)
    related_product = None

    if product:
        related_product = (
            Product.objects.filter(category=product.category)
            .exclude(id=product.id)
            .order_by('?')
            [:4]
        )
    context = {
        'product': product,
        'related_product': related_product,
    }
    return render(request, 'product_details/product_details.html', context)


def add_review(request):
    if request.method == "POST":
        full_name = request.POST["full_name"]
        title = request.POST["title"]
        content = request.POST["content"]
        rating = request.POST["rating"]
        product_id = request.POST["product_id"]

        product = get_object_or_404(Product, pk=product_id)

        if request.user.is_authenticated:
            Review.objects.create(
                user=request.user,
                full_name=full_name,
                title=title,
                content=content,
                ratings=rating,
                product=product
            )
            messages.success(request, 'Thank you for reviewing this product!')
        else:
            return HttpResponseBadRequest()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
