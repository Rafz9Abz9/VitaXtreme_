from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import PermissionDenied
from django.views.defaults import server_error

from product.models import Product
from .models import Wishlist

# Create your views here.


def add_to_wishlist(request, product_id):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, pk=product_id)
        # Authenticated user
        Wishlist.objects.get_or_create(user=request.user, product=product)
        messages.success(request, 'Product Added to Wishlist')
    else:
        # Unauthenticated user
        messages.warning(request, 'Only Authenticated User is Allowed')
        raise PermissionDenied

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_from_wishlist(request, product_id):
    if request.user.is_authenticated:
        # Authenticated user
        wishlist = get_object_or_404(
            Wishlist, product__id=product_id, user=request.user)
        wishlist.delete()
        messages.success(request, 'Product Removed from Wishlist')
    else:
        # Unauthenticated user
        messages.warning(request, 'Only Authenticated User is Allowed')
        raise PermissionDenied

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='user_auth')
def wishlist(request):
    wishlist_items = None
    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(
            user=request.user).order_by('-created_at')

    paginator = Paginator(wishlist_items, 10)
    page = request.GET.get('page')

    try:
        wishlist_items = paginator.page(page)
    except PageNotAnInteger:
        wishlist_items = paginator.page(1)
    except EmptyPage:
        wishlist_items = paginator.page(paginator.num_pages)
    context = {
        'wishlist_items': wishlist_items,
    }
    return render(request, 'wishlist/wishlist.html', context)
