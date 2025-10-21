from django.db import models
from django.conf import settings
from product.models import Product, ProductVariant


class Wishlist(models.Model):


    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='wishlist_items')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='wishlisted_products',null=True,blank=True)
    variant = models.ForeignKey(ProductVariant,on_delete=models.CASCADE,related_name='wishlisted_variants',null=True,blank=True)
    is_favorite = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'variant'],name='unique_user_variant_wishlist'),
            models.UniqueConstraint(fields=['user', 'product'],name='unique_user_product_wishlist'),
    ]
        ordering = ['-created_at']

