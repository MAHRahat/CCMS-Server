from rest_framework.permissions import BasePermission


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


class IsAnyEmployee(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_employee


class IsValidUserToCreate(BasePermission):
    def has_permission(self, request, view):
        return (not request.user.is_employee) and (request.method == 'POST')
