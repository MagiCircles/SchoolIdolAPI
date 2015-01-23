from rest_framework import permissions

class IsAdminOrSelf(permissions.BasePermission):

    def has_object_permission(self, request, view, obj=None):
        return obj is None or request.user.is_superuser or (hasattr(obj, 'owner') and obj.owner == request.user)

class UserPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method == 'POST' or request.user.is_superuser

    def has_object_permission(self, request, view, obj=None):
        return request.method == 'POST' or request.user.is_superuser or request.user == obj
