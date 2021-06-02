from rest_framework import permissions


class StaffOrReadOnly(permissions.BasePermission):
    message = 'You Don\'t Have Permission!!'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return bool(request.user.is_superuser)


class StaffOnly(permissions.BasePermission):
    message = 'You Don\'t Have Permission!!'

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.is_superuser)

    def has_object_permission(self, request, view, obj):
        return bool(request.user.is_superuser)