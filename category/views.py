from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Category
from .serializers import CategorySerializer
from rest_framework.permissions import DjangoModelPermissions


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'vendor':
            return Category.objects.filter(created_by=user)
        return Category.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)