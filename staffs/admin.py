from django.contrib import admin
from django.utils.html import format_html
from .models import Staff


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):

    list_display = (

        "photo_preview",
        "name",
        "designation",
        "is_active",

    )

    list_filter = (

        "is_active",

        "designation",

    )

    search_fields = (
        "name",
        "email",
        "phone_number",
        "designation",
    )

    ordering = (

        "name",

    )

    readonly_fields = (

        "photo_preview",

        "created_at",

        "updated_at",

    )

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "name",
                    "email",
                    "phone_number",
                    "designation",
                    "photo",
                    "photo_preview",
                )
            },
        ),

        (

            "Additional Information",

            {

                "fields": (

                    "bio",

                )

            },

        ),

        (

            "System Settings",

            {

                "fields": (

                    "is_active",

                    "created_at",

                    "updated_at",

                )

            },

        ),

    )

    def photo_preview(self, obj):

        if obj.photo:

            return format_html(

                '<img src="{}" width="80" height="80" style="border-radius:8px;" />',

                obj.photo.url,

            )

        return "-"

    photo_preview.short_description = "Photo"