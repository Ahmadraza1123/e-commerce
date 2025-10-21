from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from foodmart import views



urlpatterns = [
    path('admin/', admin.site.urls),

    path('Account/', include('Account.urls')),
    path('product/', include('product.urls')),
    path('category/', include('category.urls')),
    path('cart/', include('cart.urls')),
    path('wishlist/', include('wishlist.urls')),
    path('checkout/', include('checkout.urls')),
    path('cashcard/', include('cashcard.urls')),
path('foodmart/', views.foodmart_home, name='foodmart_home'),
path('foodmart/women/', views.women_view, name='women_page'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
