from django.contrib import admin
from django.utils.html import format_html

from .models import Notice


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "notice_type",
        "publish_date",
        "expiry_date",
        "is_public",
        "is_featured",
        "is_active",
        "attachment_link",
    )

    list_filter = (
        "notice_type",
        "is_public",
        "is_featured",
        "is_active",
        "publish_date",
    )

    search_fields = (
        "title",
        "content",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "attachment_link",
    )

    fieldsets = (
        (
            "Notice Information",
            {
                "fields": (
                    "title",
                    "notice_type",
                    "content",
                )
            },
        ),
        (
            "Attachment",
            {
                "fields": (
                    "attachment",
                    "attachment_link",
                )
            },
        ),
        (
            "Publication",
            {
                "fields": (
                    "publish_date",
                    "expiry_date",
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
        "-publish_date",
    )

    def attachment_link(self, obj):

        if obj.attachment:
            return format_html(
                '<a href="{}" target="_blank">Open Attachment</a>',
                obj.attachment.url,
            )

        return "No Attachment"

    attachment_link.short_description = "Attachment"
