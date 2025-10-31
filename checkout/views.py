import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from cart.models import Cart  # ✅ make sure it's imported
from .models import Checkout
from .serializers import CheckoutSerializer, OrderSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY


class CheckoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        cart_id = request.data.get("cart")

        # ✅ Ownership validation before serializer
        try:
            cart = Cart.objects.get(id=cart_id, user=request.user)
        except Cart.DoesNotExist:
            return Response(
                {"error": "yeh cart ap ka ni hy"},
                status=status.HTTP_403_FORBIDDEN
            )

        # ✅ Proceed normally after validation
        serializer = CheckoutSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        checkout = serializer.save()

        if checkout.payment_method == "STRIPE":
            try:
                cart_items = checkout.cart.items.all()
                total_amount = sum(item.total_price for item in cart_items)
                amount_cents = int(total_amount * 100)

                intent = stripe.PaymentIntent.create(
                    amount=amount_cents,
                    currency="usd",
                    metadata={"checkout_id": checkout.id, "user": request.user.username},
                    automatic_payment_methods={"enabled": True},
                )

                checkout.stripe_payment_intent_id = intent.id
                checkout.save()

                return Response({
                    "message": "Stripe payment initiated",
                    "client_secret": intent.client_secret,
                    "checkout_id": checkout.id,
                }, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ Process order normally (COD etc.)
        order = serializer.process_checkout(checkout)
        order_data = OrderSerializer(order, context={'request': request}).data

        return Response({
            "message": "Order created successfully",
            "order": order_data
        }, status=status.HTTP_201_CREATED)


class StripeConfirmView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        payment_intent_id = request.data.get("payment_intent_id")
        if not payment_intent_id:
            return Response({"error": "Missing payment_intent_id"}, status=400)

        try:
            # ✅ Also verify ownership (if Checkout model has user field)
            checkout = Checkout.objects.get(
                stripe_payment_intent_id=payment_intent_id,
                user=request.user
            )

            checkout.payment_status = "PAID"
            checkout.save()

            serializer = CheckoutSerializer(context={'request': request})
            order = serializer.process_checkout(checkout)
            order_data = OrderSerializer(order, context={'request': request}).data

            return Response({
                "message": "Payment confirmed, order created",
                "order": order_data
            }, status=200)

        except Checkout.DoesNotExist:
            return Response({"error": "yeh cart ap ka ni hy"}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"error": str(e)}, status=400)
