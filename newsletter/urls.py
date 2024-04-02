from django.urls import path
from . import views

urlpatterns = [
    path('subscribe', views.subscribe_newsletter, name='subscribe_newsletter'),
    path('unsubscribe', views.unsubscribe_newsletter,
         name='unsubscribe_newsletter'),
]
