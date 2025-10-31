from rest_framework import viewsets
from .serializers import ProductSerializer
from rest_framework import filters
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductVariantSerializer
from .models import ProductReview, Product


from rest_framework import viewsets, filters, permissions
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    filter_backends = [filters.SearchFilter]
    search_fields = ['product_name', 'category__category_name']

    def perform_create(self, serializer):
        # Do NOT pass created_by here; handled by serializer
        serializer.save()


class ProductReviewListView(generics.ListAPIView):
    serializer_class = ProductVariantSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        return ProductReview.objects.filter(product_id=product_id).order_by('-created_at')



class AddProductReviewView(generics.CreateAPIView):
    serializer_class = ProductVariantSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, product_id, *args, **kwargs):
        product = Product.objects.filter(id=product_id).first()
        if not product:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)


        existing_review = ProductReview.objects.filter(product=product, user=request.user).first()
        if existing_review:
            return Response({'error': 'You have already reviewed this product'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, product=product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)