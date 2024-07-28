from rest_framework import permissions


class IsOwnerOrAssignedOrReadOnly(permissions.BasePermission):
    """
    Пользовательское разрешение, создавать или редактировать только свои задания.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.assigned_to == request.user or obj.created_by == request.user or request.user.is_superuser

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False