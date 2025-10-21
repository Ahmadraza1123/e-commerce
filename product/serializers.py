from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    added_by_username = serializers.CharField(source='created_by.username', read_only=True)
    added_by_id = serializers.IntegerField(source='created_by.id', read_only=True)
    added_by_role = serializers.CharField(source='created_by.role', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'product_name',
            'category_name',
            'product_price',
            'product_image',
            'product_expiry',
            'product_quantity',
            'created_at',
            'added_by_username',
            'added_by_id',
            'added_by_role'
        ]
