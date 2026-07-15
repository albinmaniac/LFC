from django.contrib import admin
from django.utils.html import format_html

from .models import Album, Photo


class PhotoInline(admin.TabularInline):

    model = Photo
    extra = 0

    fields = (
        "image",
        "caption",
        "display_order",
        "is_active",
    )


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "event",
        "is_public",
        "is_featured",
        "is_active",
        "photo_count",
        "cover_preview",
    )

    list_filter = (
        "is_public",
        "is_featured",
        "is_active",
    )

    search_fields = (
        "title",
        "description",
    )

    autocomplete_fields = (
        "event",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "cover_preview",
    )

    inlines = [PhotoInline]

    fieldsets = (
        (
            "Album Information",
            {
                "fields": (
                    "title",
                    "description",
                    "event",
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

    def photo_count(self, obj):
        return obj.photos.count()

    photo_count.short_description = "Photos"

    def cover_preview(self, obj):

        if obj.cover_image:
            return format_html(
                '<img src="{}" width="250" />',
                obj.cover_image.url,
            )

        return "No Image"

    cover_preview.short_description = "Cover Preview"


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "album",
        "caption",
        "display_order",
        "is_active",
        "image_preview",
    )

    list_filter = (
        "is_active",
        "album",
    )

    search_fields = (
        "caption",
        "album__title",
    )

    autocomplete_fields = (
        "album",
    )

    readonly_fields = (
        "created_at",
        "image_preview",
    )

    def image_preview(self, obj):

        if obj.image:
            return format_html(
                '<img src="{}" width="200" />',
                obj.image.url,
            )

        return "No Image"

    image_preview.short_description = "Preview"
