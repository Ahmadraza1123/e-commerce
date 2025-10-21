from rest_framework import serializers
from .models import Checkout, Order, OrderItem
from decimal import Decimal
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

import random

User = get_user_model()


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'product_price', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    delivery_boy_id = serializers.IntegerField(source='delivery_boy.id', read_only=True)
    delivery_boy_name = serializers.CharField(source='delivery_boy.username', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'total_amount', 'is_paid', 'status',
            'address', 'payment_method', 'created_at',
            'delivery_boy_id', 'delivery_boy_name', 'items'
        ]
        read_only_fields = ['user', 'created_at', 'delivery_boy_id', 'delivery_boy_name']


class CheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checkout
        fields = ['id', 'user', 'cart', 'payment_method', 'payment_status', 'created_at']
        read_only_fields = ['user', 'payment_status', 'created_at']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return Checkout.objects.create(**validated_data)

    def process_checkout(self, checkout):
        cart = checkout.cart
        items = cart.items.all()
        total_amount = sum(Decimal(item.total_price or 0) for item in items)


        if checkout.payment_method == "CASHCARD" and checkout.payment_status == "PENDING":
            from cashcard.models import CashCard
            cashcard = CashCard.objects.filter(user=checkout.user).first()
            if not cashcard:
                raise serializers.ValidationError("No cashcard found for user")
            if cashcard.amount < total_amount:
                raise serializers.ValidationError("Insufficient balance")
            cashcard.amount -= total_amount
            cashcard.save()
            checkout.payment_status = "PAID"
            checkout.save()


        order = Order.objects.create(
            user=checkout.user,
            total_amount=total_amount,
            is_paid=(checkout.payment_status == "PAID"),
            status='confirmed' if checkout.payment_status == "PAID" else 'pending',
            address=getattr(checkout.user, 'address', '') or '',
            payment_method=checkout.payment_method,
        )


        for item in items:
            product_price = (
                item.variant.price if hasattr(item, 'variant') and item.variant
                else (item.product.variants.first().price if item.product.variants.exists() else 0)
            )
            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.product_name,
                product_price=Decimal(product_price),
                quantity=item.quantity,
                price=item.total_price,
            )


        delivery_boys = User.objects.filter(groups__name='delivery_boy')
        if delivery_boys.exists():
            assigned_boy = random.choice(delivery_boys)
            order.delivery_boy = assigned_boy
            order.save()

        return order