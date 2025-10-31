from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.exceptions import PermissionDenied
from .models import Category
from .serializers import CategorySerializer


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

    def perform_update(self, serializer):
        category = self.get_object()
        if self.request.user.role == "vendor" and category.created_by != self.request.user:
            raise PermissionDenied("You cannot edit another vendor's category.")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user.role == "vendor" and instance.created_by != self.request.user:
            raise PermissionDenied("You cannot delete another vendor's category.")
        instance.delete()
