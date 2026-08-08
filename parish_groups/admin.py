from django.contrib import admin

from .models import (
    ParishGroup,
    ParishGroupMember,
)


class ParishGroupMemberInline(
    admin.TabularInline
):

    model = ParishGroupMember

    extra = 0

    autocomplete_fields = [
        "member",
    ]


@admin.register(ParishGroup)
class ParishGroupAdmin(
    admin.ModelAdmin
):

    list_display = (
        "name",
        "patron_saint",
        "leader",
        "phone_number",
        "is_active",
        "member_count",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
        "patron_saint",
        "leader__first_name",
        "leader__last_name",
    )

    autocomplete_fields = (
        "leader",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    inlines = [
        ParishGroupMemberInline,
    ]

    def member_count(self, obj):
        return obj.members.filter(
            is_active=True
        ).count()

    member_count.short_description = "Members"


@admin.register(ParishGroupMember)
class ParishGroupMemberAdmin(
    admin.ModelAdmin
):

    list_display = (
        "group",
        "member",
        "role",
        "joined_date",
        "is_active",
    )

    list_filter = (
        "group",
        "role",
        "is_active",
    )

    search_fields = (
        "group__name",
        "member__first_name",
        "member__last_name",
        "member__baptism_name",
    )

    autocomplete_fields = (
        "group",
        "member",
    )

    readonly_fields = (
        "created_at",
    )
