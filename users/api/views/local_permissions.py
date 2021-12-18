from users.models import EmployeeGroup, EmployeeType, EmployeeTypePermission as ETPermission, Employee
from rest_framework import permissions
from rest_framework.request import Request


class IsSuperAdminPermission(permissions.BasePermission):
    """
    Custom permission to only allow super admin to access the view.
    """
    def has_permission(self, request: Request, view) -> bool:
        if request.user.is_superuser:
            return True
        return False


class IsBusinessOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request: Request, view: object) -> bool:
        return request.user.is_business_owner


class IsEmployee(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request: Request, view) -> bool:
        return request.user.is_employee


class EmployeeGroupPermission(permissions.BasePermission):
    """
    Custom permission to only allow owners of employee group to edit it.
    """

    def has_object_permission(self, request, view, obj: EmployeeGroup) -> bool:
        if (request.user.is_business_owner and request.user.business == obj.business) or \
                request.user.employee.employee_type.group.business == obj.business:
            return True


class EmployeeTypePermission(permissions.BasePermission):
    """
    Custom permission to only allow owners of employee type to edit it.
    """

    def has_object_permission(self, request, view, obj: EmployeeType) -> bool:
        if (request.user.is_business_owner and request.user.business == obj.group.business) or \
                request.user.employee.employee_type.group.business == obj.group.business:
            return True


class ModifyETPermission(permissions.BasePermission):
    """
    Custom permission to only allow owners of employee type to edit it.
    """

    def has_object_permission(self, request, view, obj: ETPermission) -> bool:
        if (request.user.is_business_owner and request.user.business == obj.employee_type.group.business) or \
                request.user.employee.employee_type.group.business == obj.employee_type.group.business:
            return True


class GetEmployeePermission(permissions.BasePermission):
    """
    Custom permission to only allow owners of employee type to edit it.
    """

    def has_object_permission(self, request, view, obj: Employee) -> bool:
        if request.user.is_business_owner and request.user.business == obj.employee_type.group.business:
            return True
