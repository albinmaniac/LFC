from django.db.models import Q
from accounts.models import (
    Invitation,
    LoginHistory,
    User,
    UserSession,
)
from parish.models import UserPermission


class UserReportService:
    """
    Business logic for User & Security reports.

    This service contains only ORM/business logic.
    Views must never perform database queries.
    """

    @staticmethod
    def get_login_history(search=None):
        queryset = (
            LoginHistory.objects
            .select_related("user", "session")
            .order_by("-login_time")
        )
        if search:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(user__email__icontains=search) |
                Q(ip_address__icontains=search)
            )
        return queryset

    @staticmethod
    def get_invitation_history(search=None):
        queryset = (
            Invitation.objects
            .select_related("invited_by")
            .order_by("-created_at")
        )
        if search:
            queryset = queryset.filter(
                Q(email__icontains=search) |
                Q(invited_by__email__icontains=search)
            )
        return queryset

    @staticmethod
    def get_recent_users(search=None):
        queryset = (
            User.objects
            .filter(is_active=True)
            .order_by("-date_joined")
        )
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search) |
                Q(phone_number__icontains=search)
            )
        return queryset

    @staticmethod
    def get_disabled_accounts(search=None):
        queryset = (
            User.objects
            .filter(is_active=False)
            .order_by("-date_joined")
        )
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search) |
                Q(phone_number__icontains=search)
            )
        return queryset

    @staticmethod
    def get_active_sessions(search=None):
        queryset = (
            UserSession.objects
            .filter(is_active=True)
            .select_related("user")
            .order_by("-last_activity")
        )
        if search:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(user__email__icontains=search) |
                Q(ip_address__icontains=search)
            )
        return queryset

    @staticmethod
    def get_permission_audit(search=None):
        queryset = (
            UserPermission.objects
            .select_related("user")
            .order_by(
                "user__first_name",
                "user__last_name",
                "permission",
            )
        )
        if search:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(user__email__icontains=search) |
                Q(permission__icontains=search)
            )
        return queryset