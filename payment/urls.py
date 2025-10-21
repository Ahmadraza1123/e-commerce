from django.urls import path
from .views import CreateStripePayment

urlpatterns = [
    path('create-stripe-payment/<int:order_id>/', CreateStripePayment.as_view(), name='create_stripe_payment'),
]
