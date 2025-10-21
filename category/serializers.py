from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    added_by_username = serializers.CharField(source='created_by.username', read_only=True)
    added_by_id = serializers.IntegerField(source='created_by.id', read_only=True)
    added_by_role = serializers.CharField(source='created_by.role', read_only=True)
    total_items = serializers.IntegerField(source='products.count', read_only=True)

    class Meta:
        model = Category
        fields = [
            'category_id', 'category_name', 'category_image','total_items', 'created_at',
            'added_by_username', 'added_by_id', 'added_by_role'
        ]
