from rest_framework import serializers
from .models import Product, ProductVariant, Category

import json

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['id', 'color', 'size', 'price', 'quantity']

class ProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True, required=False)
    category_name = serializers.CharField(write_only=True, required=False)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    category_display = serializers.CharField(source='category.category_name', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'product_name', 'product_description', 'product_image', 'expiry_date',
            'category_name', 'category_display', 'variants', 'created_by_name'
        ]

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user if request and request.user.is_authenticated else None

        # Extract variants from payload
        variants_data = validated_data.pop('variants', [])
        category_name = validated_data.pop('category_name', None)

        category = None
        if category_name:
            try:
                category = Category.objects.get(category_name__iexact=category_name)
            except Category.DoesNotExist:
                raise serializers.ValidationError({
                    'category_name': f"Category '{category_name}' does not exist."
                })

        product = Product.objects.create(category=category, created_by=user, **validated_data)
        print("Variant Data", variants_data)
        if isinstance(variants_data, str):
            try:
                variants_data = json.loads(variants_data)
            except json.JSONDecodeError:
                raise serializers.ValidationError({
                    'variants': 'Invalid JSON format for variants.'
                })
        for variant in variants_data:
            print("Variant", variant)
            ProductVariant.objects.create(product=product, **variant)

        product.refresh_from_db()

        return product