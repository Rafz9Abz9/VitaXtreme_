from django.urls import path
from . import views

urlpatterns = [
    path('', views.products, name='products'),
    path('<product_id>', views.product_details, name='product_details'),
    path('review/add', views.add_review, name='add_review'),
]
