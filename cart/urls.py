from django.urls import path
from .views import AddToCartView,RemoveFromCartView

urlpatterns = [
    path('add/<int:product_id>/', AddToCartView.as_view(), name='add-to-cart'),
    path('remove/<int:variant_id>/', RemoveFromCartView.as_view(), name='remove-from-cart'),

    # path('crud/', CartCRUDView.as_view(), name='cart-detail'),
    # path('crud/<int:pk>/', CartCRUDView.as_view(), name='cart-specific'),

]

