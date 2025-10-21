from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'customer', 'product', 'quantity', 'total_price', 'status', 'created_at']
        read_only_fields = ['customer', 'total_price', 'status', 'created_at']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        validated_data['customer'] = user
        return super().create(validated_data)

