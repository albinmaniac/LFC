from django.contrib import admin

from .models import Family, FamilyMember, FamilyUnit


class FamilyMemberInline(admin.TabularInline):
    model = FamilyMember
    extra = 0
    fields = (
        "first_name",
        "last_name",
        "relationship",
        "phone_number",
        "is_family_head",
        "is_active",
    )


@admin.register(FamilyUnit)
class FamilyUnitAdmin(admin.ModelAdmin):
    list_display = (
        "family_unit_name",
        "saint",
        "president",
        "secretary",
        "is_active",
    )

    search_fields = (
        "family_unit_name",
        "saint",
    )

    list_filter = (
        "is_active",
    )

    ordering = (
        "family_unit_name",
    )


@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    list_display = (
        "house_name",
        "family_unit",
        "family_head_name",
        "ward_number",
        "is_active",
    )

    search_fields = (
        "house_name",
    )

    list_filter = (
        "family_unit",
        "is_active",
    )

    ordering = (
        "house_name",
    )

    def family_head_name(self, obj):
        head = obj.members.filter(
            is_family_head=True,
            is_active=True,
        ).first()

        if head:
            return f"{head.first_name} {head.last_name}".strip()

        return "-"

    family_head_name.short_description = "Family Head"

    inlines = [FamilyMemberInline]


@admin.register(FamilyMember)
class FamilyMemberAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "family",
        "relationship",
        "is_family_head",
        "is_active",
    )

    search_fields = (
        "first_name",
        "last_name",
        "phone_number",
        "email",
    )

    list_filter = (
        "relationship",
        "gender",
        "is_family_head",
        "is_active",
    )

    autocomplete_fields = (
        "family",
    )
