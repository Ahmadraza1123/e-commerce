from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'id',
            'user',
            'order',
            'amount',
            'stripe_payment_intent',
            'status',
            'created_at'
        ]
        read_only_fields = ['user', 'stripe_payment_intent', 'status', 'created_at']

    def create(self, validated_data):
        """
        Automatically attach the logged-in user when creating a payment.
        """
        request = self.context.get('request')
        user = request.user
        validated_data['user'] = user
        return super().create(validated_data)
