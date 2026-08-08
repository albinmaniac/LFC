from rest_framework import serializers
from families.models import Family, FamilyMember, FamilyUnit


class FamilyDirectoryReportSerializer(serializers.ModelSerializer):
    """
    Serializer for the Family Directory report.
    """

    family_unit = serializers.CharField(
        source="family_unit.family_unit_name",
        read_only=True,
    )

    head_of_family = serializers.SerializerMethodField()

    total_members = serializers.SerializerMethodField()

    class Meta:
        model = Family

        fields = (
            "id",
            "house_name",
            "address",
            "ward_number",
            "family_unit",
            "head_of_family",
            "total_members",
            "is_active",
            "created_at",
            "updated_at",
        )

        read_only_fields = fields

    def get_head_of_family(self, obj):
        head = obj.members.filter(
            is_family_head=True,
            is_active=True,
        ).first()

        if not head:
            return None

        return f"{head.first_name} {head.last_name}".strip()

    def get_total_members(self, obj):
        return obj.members.filter(
            is_active=True,
        ).count()


# Family Unit Report Serializer
class FamilyUnitReportSerializer(serializers.ModelSerializer):
    """
    Serializer for the Family Unit report.
    """

    president_name = serializers.SerializerMethodField()
    secretary_name = serializers.SerializerMethodField()

    total_families = serializers.IntegerField(read_only=True)
    total_members = serializers.IntegerField(read_only=True)

    class Meta:
        model = FamilyUnit

        fields = (
            "id",
            "family_unit_name",
            "saint",
            "phone_number",
            "president_name",
            "secretary_name",
            "total_families",
            "total_members",
            "is_active",
            "created_at",
            "updated_at",
        )

        read_only_fields = fields

    def get_president_name(self, obj):
        if not obj.president:
            return None
        return obj.president.full_name or obj.president.email

    def get_secretary_name(self, obj):
        if not obj.secretary:
            return None
        return obj.secretary.full_name or obj.secretary.email


class FamilyHeadReportSerializer(serializers.ModelSerializer):
    """
    Serializer for the Family Heads report.
    """

    family_unit = serializers.CharField(
        source="family.family_unit.family_unit_name",
        read_only=True,
    )

    house_name = serializers.CharField(
        source="family.house_name",
        read_only=True,
    )

    full_name = serializers.SerializerMethodField()

    class Meta:
        model = FamilyMember

        fields = (
            "id",
            "full_name",
            "phone_number",
            "email",
            "house_name",
            "family_unit",
            "occupation",
            "is_active",
            "created_at",
            "updated_at",
        )

        read_only_fields = fields

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()


class FamilyMemberReportSerializer(serializers.ModelSerializer):
    """
    Serializer for the Family Members report.
    """

    family_unit = serializers.CharField(
        source="family.family_unit.family_unit_name",
        read_only=True,
    )

    house_name = serializers.CharField(
        source="family.house_name",
        read_only=True,
    )

    full_name = serializers.SerializerMethodField()

    class Meta:
        model = FamilyMember

        fields = (
            "id",
            "full_name",
            "gender",
            "relationship",
            "phone_number",
            "email",
            "occupation",
            "house_name",
            "family_unit",
            "is_family_head",
            "is_active",
            "created_at",
            "updated_at",
        )

        read_only_fields = fields

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()
