from rest_framework import permissions

class IsAuthenticatedSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
       return request.user.is_superuser

class IsActive(permissions.BasePermission):
    def has_permission(self, request, view):
       return request.user.is_active