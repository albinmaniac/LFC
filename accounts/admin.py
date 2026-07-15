from django.contrib import admin

from .models import User, Invitation,LoginHistory,UserSession


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
        "role",
        "is_active",
    )

    search_fields = (
        "email",
        "first_name",
        "last_name",
    )

    list_filter = (
        "role",
        "is_active",
        "is_staff",
        "is_superuser",
    )


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "role",
        "created_at",
    )

    search_fields = (
        "email",
    )

@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "session_id",
        "ip_address",
        "is_active",
        "last_activity",
        "created_at",
    )

    search_fields = (
        "user__email",
        "session_id",
        "ip_address",
    )

    list_filter = (
        "is_active",
        "created_at",
    )

    readonly_fields = (
        "session_id",
        "created_at",
        "last_activity",
    )


@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "session",
        "ip_address",
        "login_time",
        "logout_time",
        "is_successful",
    )

    search_fields = (
        "user__email",
        "ip_address",
    )

    list_filter = (
        "is_successful",
        "login_time",
    )

    readonly_fields = (
        "login_time",
        "logout_time",
    )