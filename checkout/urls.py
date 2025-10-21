from django.urls import path
from .views import CheckoutView, StripeConfirmView

urlpatterns = [

    path('create/', CheckoutView.as_view(), name='checkout-create'),

    path('confirm/', StripeConfirmView.as_view(), name='stripe-confirm'),
]
