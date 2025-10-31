from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet
from .views import ProductReviewListView, AddProductReviewView


router = DefaultRouter()
router.register(r'crud', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('reviews/<int:product_id>/', ProductReviewListView.as_view(), name='product-reviews'),
    path('reviews/add/<int:product_id>/', AddProductReviewView.as_view(), name='add-product-review'),
]