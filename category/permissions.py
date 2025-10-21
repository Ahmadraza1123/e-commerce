from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission: Only the creator (owner) can edit/delete their categories.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return obj.created_by == request.user or request.user.is_superuser

        return obj.created_by == request.user or request.user.is_superuser
