from rest_framework import generics, permissions
from rest_framework.response import Response
from django.db import transaction
from .models import Cart, CartItem
from .serializers import CartSerializer, SimpleCartItemSerializer
from product.models import Product, ProductVariant
from rest_framework.permissions import DjangoModelPermissions


class AddToCartView(generics.CreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = SimpleCartItemSerializer
    permission_classes = [permissions.IsAuthenticated, DjangoModelPermissions]

    def post(self, request, product_id):
        user = request.user
        cart = Cart.objects.create(user=user)

        variant_id = request.data.get("variant_id")
        quantity = int(request.data.get("quantity", 1))

        product = Product.objects.filter(id=product_id).first()
        if not product:
            return Response({"error": "Product not found"}, status=404)

        variant = ProductVariant.objects.filter(id=variant_id, product=product).first()
        if not variant:
            return Response({"error": "Invalid variant for this product"}, status=400)

        if variant.quantity < quantity:
            return Response(
                {"error": f"Only {variant.quantity} items available in stock."},
                status=400
            )

        with transaction.atomic():
            cart_item = CartItem.objects.create(
                cart=cart,
                product=product,
                variant=variant,
                quantity=quantity
            )
            variant.quantity -= quantity
            variant.save()

        response_data = SimpleCartItemSerializer(cart_item).data
        response_data["cart_id"] = cart.id
        return Response(response_data, status=201)


class CartCRUDView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated, DjangoModelPermissions]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user).order_by('-id')

    def get_object(self):
        pk = self.kwargs.get('pk')
        if pk:
            return self.get_queryset().filter(pk=pk).first()
        return self.get_queryset().first()

    def get(self, request, *args, **kwargs):

        if request.query_params.get('all') == 'true':
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        instance = self.get_object()
        if not instance:
            return Response({"error": "Cart not found."}, status=404)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return Response({"error": "Cart not found."}, status=404)

        items_data = request.data.get("items", [])
        for item_data in items_data:
            variant_id = item_data.get("variant_id")
            new_quantity = int(item_data.get("quantity", 0))

            if new_quantity <= 0:
                return Response(
                    {"error": "Quantity 0 or negative is not allowed."},
                    status=400
                )

            cart_item = instance.items.filter(variant__id=variant_id).first()
            if not cart_item:
                return Response(
                    {"error": f"Variant ID {variant_id} not found in this cart."},
                    status=400
                )

            variant = cart_item.variant
            old_quantity = cart_item.quantity
            diff = new_quantity - old_quantity

            if diff > 0:
                if variant.quantity < diff:
                    return Response(
                        {"error": f"Only {variant.quantity} more available in stock."},
                        status=400
                    )
                variant.quantity -= diff
            elif diff < 0:
                variant.quantity += abs(diff)

            variant.save()
            cart_item.quantity = new_quantity
            cart_item.save()

        instance.refresh_from_db()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return Response({"error": "Cart not found."}, status=404)

        for item in instance.items.all():
            variant = item.variant
            variant.quantity += item.quantity
            variant.save()

        instance.delete()
        return Response(
            {"message": "Cart deleted and stock restored successfully."},
            status=200
        )
