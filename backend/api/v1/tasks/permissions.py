from rest_framework import permissions

class IsTaskOwnerOrForbidden(permissions.BasePermission):
    """Права на задачу. Владелец или запрещено."""
    def has_object_permission(self, request, view, obj):
        """Права на объект."""
        return obj.user == request.user

