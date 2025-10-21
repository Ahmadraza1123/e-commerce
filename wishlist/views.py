from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Wishlist
from .serializers import WishlistSerializer
from product.models import Product, ProductVariant


class WishlistListView(generics.ListAPIView):

    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)


class AddToWishlistView(generics.CreateAPIView):
    """Add product or variant to wishlist (with optional comment)."""
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        product_id = request.data.get("product_id")
        variant_id = request.data.get("variant_id")

        product = Product.objects.filter(id=product_id).first() if product_id else None
        variant = ProductVariant.objects.filter(id=variant_id).first() if variant_id else None

        if not product and not variant:
            return Response(
                {"error": "You must provide either product_id or variant_id"},
                status=status.HTTP_400_BAD_REQUEST
            )

        wishlist_item, created = Wishlist.objects.get_or_create(
            user=user,
            product=product,
            variant=variant,
            defaults={'is_favorite': True}
        )

        if not created:
            # Toggle favorite status if already exists
            wishlist_item.is_favorite = not wishlist_item.is_favorite
            wishlist_item.save()
            msg = "Removed from favorites" if not wishlist_item.is_favorite else "Added to favorites"
            return Response({"message": msg}, status=status.HTTP_200_OK)

        serializer = self.get_serializer(wishlist_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RemoveFromWishlistView(generics.DestroyAPIView):
    """Remove a product or variant from wishlist."""
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        product_id = request.data.get("product_id")
        variant_id = request.data.get("variant_id")

        wishlist_item = Wishlist.objects.filter(user=request.user,product_id=product_id if product_id else None,variant_id=variant_id if variant_id else None).first()

        if not wishlist_item:
            return Response({"error": "Item not found in wishlist"}, status=status.HTTP_404_NOT_FOUND)

        wishlist_item.delete()
        return Response({"message": "Removed from wishlist"}, status=status.HTTP_204_NO_CONTENT)
