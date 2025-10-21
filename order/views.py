from rest_framework import viewsets, permissions
from .models import Order
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_staff and not user.groups.filter(name='Vendor').exists():
            return Order.objects.filter(customer=user)
        return Order.objects.all()

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

