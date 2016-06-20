from rest_framework import permissions

def shouldSelectOwner(request):
    return (request.resolver_match.url_name.endswith('-detail')
            and request.method not in permissions.SAFE_METHODS
            and not request.user.is_staff)

class IsStaffOrSelf(permissions.BasePermission):

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj=None):
        return (
            request.method in permissions.SAFE_METHODS
            or obj is None
            or request.user.is_staff
            or obj.owner == request.user
        )

class IsStaffOrReadOnly(permissions.BasePermission):

     def has_permission(self, request, view):
         return (
             request.method in permissions.SAFE_METHODS
             or (request.user
                 and request.user.is_authenticated()
                 and request.user.is_staff
         ))

class UserPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj=None):
        return (
            request.method in permissions.SAFE_METHODS
            or obj is None
            or request.user.is_staff
            or obj == request.user
        )
