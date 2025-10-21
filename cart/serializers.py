from decimal import Decimal
from rest_framework import serializers
from .models import Cart, CartItem


class SimpleCartItemSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(source='product.category.id', read_only=True)
    category_name = serializers.CharField(source='product.category.category_name', read_only=True)
    variant_id = serializers.IntegerField(source='variant.id', read_only=True)
    variant_color = serializers.CharField(source='variant.color', read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            'category_id',
            'category_name',
            'variant_id',
            'variant_color',
            'quantity',
            'total_price',
        ]

    def get_total_price(self, obj):
        return Decimal(obj.total_price)


class CartSerializer(serializers.ModelSerializer):
    cart_id = serializers.IntegerField(source='id', read_only=True)
    customer_id = serializers.IntegerField(source='user.id', read_only=True)
    customer_name = serializers.CharField(source='user.username', read_only=True)
    items = SimpleCartItemSerializer(many=True)
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            'cart_id',
            'customer_id',
            'customer_name',
            'items',
            'total_amount',
        ]

    def get_total_amount(self, obj):
        return Decimal(obj.total)

    def update(self, instance, validated_data):

        items_data = self.initial_data.get('items', [])

        for item_data in items_data:
            variant_id = item_data.get('variant_id')
            new_quantity = int(item_data.get('quantity', 0))

            if not variant_id:
                continue

            cart_item = instance.items.filter(variant__id=variant_id).first()
            if not cart_item:
                raise serializers.ValidationError({
                    "error": f"Variant ID {variant_id} not found in this cart."
                })

            if new_quantity <= 0:
                raise serializers.ValidationError({
                    "error": "Quantity must be greater than 0."
                })

            variant = cart_item.variant
            old_quantity = cart_item.quantity
            stock_available = variant.quantity


            diff = new_quantity - old_quantity

            if diff > 0:

                if stock_available < diff:
                    raise serializers.ValidationError({
                        "error": f"Only {stock_available} items available in stock."
                    })
                variant.quantity -= diff
            elif diff < 0:

                variant.quantity += abs(diff)

            variant.save()
            cart_item.quantity = new_quantity
            cart_item.save()

        instance.refresh_from_db()
        return instance
