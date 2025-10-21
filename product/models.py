from django.db import models
from django.conf import settings

class Product(models.Model):
    product_name = models.CharField(max_length=100)
    category_name = models.CharField(max_length=100)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_image = models.ImageField(upload_to='product_images/')
    product_expiry = models.DateField()
    product_quantity = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)