from django.contrib import admin
from django.utils.html import format_html

from .models import Parish, UserPermission


@admin.register(Parish)
class ParishAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "phone",
        "email",
        "updated_at",
    )

    readonly_fields = (
        "logo_preview",
        "cover_preview",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "name",
                    "address",
                    "phone",
                    "email",
                    "website",
                )
            },
        ),
        (
            "Media",
            {
                "fields": (
                    "logo",
                    "logo_preview",
                    "cover_image",
                    "cover_preview",
                )
            },
        ),
        (
            "Content",
            {
                "fields": (
                    "history",
                    "mission",
                    "vision",
                )
            },
        ),
        (
            "System Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" width="100" />',
                obj.logo.url,
            )
        return "-"

    logo_preview.short_description = "Logo Preview"

    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html(
                '<img src="{}" width="250" />',
                obj.cover_image.url,
            )
        return "-"
    

    def has_add_permission(self, request):

        if Parish.objects.exists():

            return False

        return super().has_add_permission(request)
       


# Register UserPermission model
@admin.register(UserPermission)
class UserPermissionAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "permission",
        "created_at",
    )

    list_filter = (
        "permission",
    )

    search_fields = (
        "user__email",
        "user__first_name",
        "user__last_name",
    )

    autocomplete_fields = (
        "user",
    )

    ordering = (
        "user",
        "permission",
    )