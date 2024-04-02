from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import custom_400_view, custom_404_view, custom_403_view, custom_500_view
from django.conf.urls import handler400, handler404, handler403, handler500
from user.views import VerificationView

handler400 = custom_400_view
handler403 = custom_403_view
handler404 = custom_404_view
handler500 = custom_500_view

urlpatterns = [
    path('', include('core.urls')),
    path('user/', include('user.urls')),
    path('products/', include('product.urls')),
    path('cart/', include('cart.urls')),
    path('wishlist/', include('wishlist.urls')),
    path('checkout/', include('checkout.urls')),
    path('newsletter/', include('newsletter.urls')),
    path('activate/<uidb64>/<token>', VerificationView.as_view(), name='activate'),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
