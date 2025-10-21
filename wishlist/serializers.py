from rest_framework import serializers
from .models import Wishlist

class WishlistSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.product_name', read_only=True)
    product_price = serializers.DecimalField(source='product.product_price', read_only=True, max_digits=10, decimal_places=2)

    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'product', 'product_name', 'product_price', 'created_at']
        read_only_fields = ['user', 'created_at']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)
