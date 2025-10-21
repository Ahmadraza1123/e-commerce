from rest_framework import serializers
from .models import Product, ProductVariant, Category, ProductReview
import json
from wishlist.models import Wishlist



class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['id', 'color', 'size', 'price', 'quantity']


class ProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True, read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    created_by_role = serializers.CharField(source='created_by.role', read_only=True)


    # 👇 user category name input karega instead of id
    category_name = serializers.CharField(write_only=True, required=False)

    # 👇 response me category ka naam dikhega
    category_display = serializers.CharField(source='category.category_name', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'product_name',
            'category_name',       # input (write-only)
            'category_display',    # output (read-only)
            'product_description',
            'product_image',
            'expiry_date',
            'variants',
            'created_at',
            'created_by_name',
            'created_by_role'
        ]

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user if request else None
        category_name = validated_data.pop('category_name', None)
        category = None

        # 🔍 Check if category exists
        if category_name:
            try:
                category = Category.objects.get(category_name__iexact=category_name)
            except Category.DoesNotExist:
                raise serializers.ValidationError(
                    {"category_name": f"Category '{category_name}' does not exist."}
                )

            # 🚫 Check: vendor can only use their own category
            if user.role == "vendor" and category.created_by != user:
                raise serializers.ValidationError(
                    {"category_name": "You cannot add a product to another vendor's category."}
                )

        # ✅ Create product safely
        product = Product.objects.create(created_by=user, category=category, **validated_data)

        # ✅ Handle variants (optional)
        variants_data = request.data.get('variants', None)
        if variants_data:
            try:
                if isinstance(variants_data, str):
                    variants_list = json.loads(variants_data)
                else:
                    variants_list = variants_data
                for variant in variants_list:
                    ProductVariant.objects.create(product=product, **variant)
            except Exception as e:
                print("Variant JSON parse error:", e)

        return product


class ProductReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = ProductReview
        fields = ['id', 'user', 'user_name', 'product', 'rating', 'comment', 'created_at']
        read_only_fields = ['user', 'created_at']
