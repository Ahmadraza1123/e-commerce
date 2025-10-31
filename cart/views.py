from django.db import transaction
from .serializers import SimpleCartItemSerializer
from product.models import Product, ProductVariant
from rest_framework.permissions import DjangoModelPermissions
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Cart, CartItem


class AddToCartView(generics.CreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = SimpleCartItemSerializer
    permission_classes = [permissions.IsAuthenticated, DjangoModelPermissions]

    def post(self, request, product_id):
        user = request.user

        # 🔹 Get existing open cart or create new one if none exists
        cart = Cart.objects.filter(user=user, is_locked=False).first()
        if not cart:
            cart = Cart.objects.create(user=user)

        variant_id = request.data.get("variant_id")
        quantity = int(request.data.get("quantity", 1))

        # 🔹 Check product
        product = Product.objects.filter(id=product_id).first()
        if not product:
            return Response({"error": "Product not found"}, status=404)

        # 🔹 Check variant
        variant = ProductVariant.objects.filter(id=variant_id, product=product).first()
        if not variant:
            return Response({"error": "Invalid variant for this product"}, status=400)

        # 🔹 Check stock availability
        if variant.quantity < quantity:
            return Response(
                {"error": f"Only {variant.quantity} items available in stock."},
                status=400
            )

        # 🔹 Check if item already exists in the cart
        existing_item = CartItem.objects.filter(cart=cart, variant=variant).first()
        if existing_item:

            total_quantity = existing_item.quantity + quantity
            if variant.quantity < quantity:
                return Response(
                    {"error": f"Only {variant.quantity} more available in stock."},
                    status=400
                )
            variant.quantity -= quantity
            variant.save()
            existing_item.quantity = total_quantity
            existing_item.save()
            message = "Item quantity updated in cart."
        else:
            # Create new item
            with transaction.atomic():
                CartItem.objects.create(
                    cart=cart,
                    product=product,
                    variant=variant,
                    quantity=quantity
                )
                variant.quantity -= quantity
                variant.save()
            message = "Item added to cart."

        # 🔹 Response
        response_data = {
            "message": message,
            "cart_id": cart.id,
            "items": SimpleCartItemSerializer(cart.items.all(), many=True).data
        }
        return Response(response_data, status=201)

class RemoveFromCartView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, variant_id, *args, **kwargs):
        user = request.user
        cart = Cart.objects.filter(user=user).first()

        if not cart:
            return Response({"message": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            item = CartItem.objects.get(cart=cart, variant_id=variant_id)
            item.delete()
            return Response({"message": "Item removed from cart."}, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            return Response({"message": "Item not found in cart."}, status=status.HTTP_404_NOT_FOUND)

class UpdateCartItemQuantityView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, variant_id, *args, **kwargs):
        user = request.user
        new_quantity = request.data.get("quantity")

        if not new_quantity or int(new_quantity) <= 0:
            return Response({"message": "Invalid quantity."}, status=status.HTTP_400_BAD_REQUEST)

        cart = Cart.objects.filter(user=user).first()
        if not cart:
            return Response({"message": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            item = CartItem.objects.get(cart=cart, variant_id=variant_id)
            item.quantity = int(new_quantity)
            item.save()
            return Response({
                "message": "Cart item quantity updated.",
                "variant_id": variant_id,
                "new_quantity": item.quantity
            }, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            return Response({"message": "Item not found in cart."}, status=status.HTTP_404_NOT_FOUND)