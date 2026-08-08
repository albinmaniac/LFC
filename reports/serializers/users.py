

from rest_framework import serializers

from accounts.models import (
    Invitation,
    LoginHistory,
    User,
    UserSession,
)
from parish.models import UserPermission


class LoginHistoryReportSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = LoginHistory
        fields = (
            "id",
            "user_name",
            "ip_address",
            "user_agent",
            "login_time",
            "logout_time",
            "is_successful",
        )
        read_only_fields = fields

    def get_user_name(self, obj):
        return obj.user.full_name or obj.user.email


class InvitationReportSerializer(serializers.ModelSerializer):
    invited_by = serializers.EmailField(source="invited_by.email", read_only=True)

    class Meta:
        model = Invitation
        fields = (
            "id",
            "email",
            "role",
            "status",
            "invited_by",
            "expires_at",
            "created_at",
        )
        read_only_fields = fields


class RecentUserReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "full_name",
            "email",
            "role",
            "phone_number",
            "is_active",
            "is_email_verified",
            "date_joined",
        )
        read_only_fields = fields


class ActiveSessionReportSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = UserSession
        fields = (
            "id",
            "user_name",
            "ip_address",
            "user_agent",
            "last_activity",
            "is_active",
            "created_at",
        )
        read_only_fields = fields

    def get_user_name(self, obj):
        return obj.user.full_name or obj.user.email


class PermissionAuditReportSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    permission_display = serializers.CharField(source="get_permission_display", read_only=True)

    class Meta:
        model = UserPermission
        fields = (
            "id",
            "user_name",
            "permission",
            "permission_display",
            "created_at",
        )
        read_only_fields = fields

    def get_user_name(self, obj):
        return obj.user.full_name or obj.user.email