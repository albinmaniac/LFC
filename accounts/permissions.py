from rest_framework.permissions import BasePermission

from .models import UserRole
from parish.models import UserPermission


def has_permission(
        user,
        permission_name,
    ):

    if not user.is_authenticated:
        return False

    if not user.is_active:
        return False

    if user.role == UserRole.SUPERADMIN:
        return True

    return UserPermission.objects.filter(
        user=user,
        permission=permission_name,
    ).exists()


# ------------------------------------------------------------------
# System Role Permissions
# ------------------------------------------------------------------
class IsSuperAdmin(BasePermission):
    """Allows access only to SuperAdmins."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_active
            and request.user.role == UserRole.SUPERADMIN
        )


class IsStaffOrSuperAdmin(BasePermission):
    """Allows access to Staff and SuperAdmins."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_active
            and request.user.role in [
                UserRole.SUPERADMIN,
                UserRole.STAFF,
            ]
        )


class IsGroupLeader(BasePermission):
    """Allows access only to Group Leaders."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_active
            and request.user.role == UserRole.GROUP_LEADER
        )


class IsFamilyUnitPresident(BasePermission):
    """Allows access only to Family Unit Presidents."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_active
            and request.user.role == UserRole.FAMILY_UNIT_PRESIDENT
        )


# ------------------------------------------------------------------
# Feature Permissions
# ------------------------------------------------------------------
class CanManageParish(BasePermission):
    """Allows users to manage parish information."""

    def has_permission(self, request, view):
        return has_permission(
            request.user,
            UserPermission.PermissionChoices.MANAGE_PARISH,
        )


# Dashboard permission class
class CanViewDashboard(BasePermission):
    """Allows users with dashboard permission."""

    def has_permission(self, request, view):
        return has_permission(
            request.user,
            UserPermission.PermissionChoices.VIEW_DASHBOARD,
        )


class CanManageFamilyUnits(BasePermission):
    """Allows users to manage family units."""

    def has_permission(self, request, view):
        return has_permission(
            request.user,
            UserPermission.PermissionChoices.MANAGE_FAMILY_UNITS,
        )


class CanManageFamilies(BasePermission):
    """Allows users to manage families."""

    def has_permission(self, request, view):
        return has_permission(
            request.user,
            UserPermission.PermissionChoices.MANAGE_FAMILIES,
        )



class CanManageFamilyMembers(BasePermission):
    """Allows users to manage family members."""

    def has_permission(self, request, view):
        return has_permission(
            request.user,
            UserPermission.PermissionChoices.MANAGE_FAMILY_MEMBERS,
        )


# Parish Groups permission class
class CanManageGroups(BasePermission):
    """Allows users to manage parish groups."""

    def has_permission(self, request, view):
        return has_permission(
            request.user,
            UserPermission.PermissionChoices.MANAGE_GROUPS,
        )


class CanManageEvents(BasePermission):
    """Allows users to manage events."""

    def has_permission(self, request, view):
        return has_permission(
            request.user,
            UserPermission.PermissionChoices.MANAGE_EVENTS,
        )


class CanManageNotices(BasePermission):
    """Allows users to manage notices."""

    def has_permission(self, request, view):
        return has_permission(
            request.user,
            UserPermission.PermissionChoices.MANAGE_NOTICES,
        )


class CanManageGallery(BasePermission):
    """Allows users to manage gallery items."""

    def has_permission(self, request, view):
        return has_permission(
            request.user,
            UserPermission.PermissionChoices.MANAGE_GALLERY,
        )


# ------------------------------------------------------------------
# Settings, Security & Reports
# ------------------------------------------------------------------
class CanManageSettings(BasePermission):
    """Allows users to manage mass timings and settings assigned through permissions."""

    def has_permission(self, request, view):
        return has_permission(
            request.user,
            UserPermission.PermissionChoices.MANAGE_SETTINGS,
        )


class CanManageSecurity(BasePermission):
    """Allows users to access security features."""

    def has_permission(self, request, view):
        return has_permission(
            request.user,
            UserPermission.PermissionChoices.MANAGE_SECURITY,
        )


class CanManagePermissions(BasePermission):
    """Allows users to manage user permissions."""

    def has_permission(self, request, view):
        return has_permission(
            request.user,
            UserPermission.PermissionChoices.MANAGE_PERMISSIONS,
        )


class CanViewReports(BasePermission):
    """Allows users to view reports."""

    def has_permission(self, request, view):
        return has_permission(
            request.user,
            UserPermission.PermissionChoices.VIEW_REPORTS,
        )