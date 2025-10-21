from rest_framework import serializers
from .models import Wishlist
from product.serializers import ProductSerializer, ProductVariantSerializer


class WishlistSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    variant = ProductVariantSerializer(read_only=True)

    class Meta:
        model = Wishlist
        fields = [
            'id',
            'user',
            'product',
            'variant',
            'is_favorite',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']
