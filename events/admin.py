from django.contrib import admin
from django.utils.html import format_html

from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "event_type",
        "family_unit",
        "start_datetime",
        "is_public",
        "is_featured",
        "is_active",
    )

    list_filter = (
        "event_type",
        "is_public",
        "is_featured",
        "is_active",
        "start_datetime",
    )

    search_fields = (
        "title",
        "venue",
        "description",
    )

    autocomplete_fields = (
        "family_unit",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "cover_preview",
    )

    fieldsets = (
        (
            "Event Information",
            {
                "fields": (
                    "title",
                    "event_type",
                    "family_unit",
                    "description",
                    "venue",
                )
            },
        ),
        (
            "Schedule",
            {
                "fields": (
                    "start_datetime",
                    "end_datetime",
                )
            },
        ),
        (
            "Media",
            {
                "fields": (
                    "cover_image",
                    "cover_preview",
                )
            },
        ),
        (
            "Status",
            {
                "fields": (
                    "is_public",
                    "is_featured",
                    "is_active",
                )
            },
        ),
        (
            "Audit",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    ordering = (
        "-start_datetime",
    )

    def cover_preview(self, obj):

        if obj.cover_image:
            return format_html(
                '<img src="{}" width="250" />',
                obj.cover_image.url,
            )

        return "No Image"

    cover_preview.short_description = "Cover Preview"

