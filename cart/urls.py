from django.urls import path
from .views import AddToCartView, CartCRUDView

urlpatterns = [
    path('add/<int:product_id>/', AddToCartView.as_view(), name='add-to-cart'),
    path('crud/', CartCRUDView.as_view(), name='cart-detail'),
    path('crud/<int:pk>/', CartCRUDView.as_view(), name='cart-specific'),

]

