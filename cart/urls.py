from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/', views.update_cart_product_quantity,
         name='update_cart_product_quantity'),
    path('cart/remove/<product_id>',
         views.remove_from_cart, name='remove_from_cart'),
]
