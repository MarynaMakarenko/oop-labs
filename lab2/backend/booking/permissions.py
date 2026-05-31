from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """Allow access only to users with role='admin'."""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_admin())


class IsClient(BasePermission):
    """Allow access only to users with role='client'."""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_client())


class IsOwnerOrAdmin(BasePermission):
    """Object-level: owner or admin can access."""

    def has_object_permission(self, request, view, obj):
        if request.user.is_admin():
            return True
        owner = getattr(obj, 'client', getattr(obj, 'user', None))
        return owner == request.user
