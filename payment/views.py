import stripe
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from order.models import Order
from .models import Payment

stripe.api_key = "your_stripe_secret_key"

class CreateStripePayment(APIView):
    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, customer=request.user)
            intent = stripe.PaymentIntent.create(
                amount=int(order.total_price * 100),
                currency="usd",
                metadata={'order_id': order.id},
            )
            payment = Payment.objects.create(
                user=request.user,
                order=order,
                amount=order.total_price,
                stripe_payment_intent=intent['id']
            )
            return Response({'client_secret': intent['client_secret']})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
