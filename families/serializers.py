from rest_framework import serializers

from .models import Family, FamilyMember, FamilyUnit


class FamilyUnitSerializer(serializers.ModelSerializer):
    saint_photo_url = serializers.SerializerMethodField()
    president_name = serializers.SerializerMethodField()
    secretary_name = serializers.SerializerMethodField()
    family_count = serializers.SerializerMethodField()

    class Meta:
        model = FamilyUnit

        fields = (
            "id",
            "family_unit_name",
            "saint",
            "saint_photo",
            "saint_photo_url",
            "president",
            "president_name",
            "secretary",
            "secretary_name",
            "family_count",
            "phone_number",
            "is_active",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )

    def validate_family_unit_name(self, value):
        value = value.strip()

        if len(value) < 2:
            raise serializers.ValidationError(
                "Family unit name must contain at least 2 characters."
            )

        return value

    def validate_saint(self, value):
        value = value.strip()

        if len(value) < 2:
            raise serializers.ValidationError(
                "Saint name must contain at least 2 characters."
            )

        return value

    def get_saint_photo_url(self, obj):

        request = self.context.get("request")

        if obj.saint_photo:

            if request:
                return request.build_absolute_uri(
                    obj.saint_photo.url
                )

            return obj.saint_photo.url

        return None

    def get_president_name(self, obj):
        if obj.president:
            return (
                f"{obj.president.first_name} "
                f"{obj.president.last_name}"
            ).strip()
        return None

    def get_secretary_name(self, obj):
        if obj.secretary:
            return (
                f"{obj.secretary.first_name} "
                f"{obj.secretary.last_name}"
            ).strip()
        return None

    def get_family_count(self, obj):
        return obj.families.filter(
            is_active=True
        ).count()


class FamilySerializer(serializers.ModelSerializer):
    family_head_name = serializers.SerializerMethodField()
    family_phone_number = serializers.SerializerMethodField()
    family_email = serializers.SerializerMethodField()
    family_unit_name = serializers.CharField(
        source="family_unit.family_unit_name",
        read_only=True,
    )

    class Meta:
        model = Family
        fields = (
            "id",
            "family_unit",
            "family_unit_name",
            "family_head_name",
            "family_phone_number",
            "family_email",
            "house_name",
            "address",
            "ward_number",
            "is_active",
            "created_at",
            "updated_at",
        )

    def get_family_head_name(self, obj):
        head = obj.members.filter(
            is_family_head=True,
            is_active=True,
        ).first()

        if head:
            return (
                f"{head.first_name} "
                f"{head.last_name}"
            ).strip()

        return None

    def get_family_phone_number(self, obj):
        head = obj.members.filter(
            is_family_head=True,
            is_active=True,
        ).first()

        return head.phone_number if head else None

    def get_family_email(self, obj):
        head = obj.members.filter(
            is_family_head=True,
            is_active=True,
        ).first()

        return head.email if head else None

    def validate_house_name(self, value):
        value = value.strip()

        if len(value) < 2:
            raise serializers.ValidationError(
                "House name must contain at least 2 characters."
            )

        return value


    def validate_ward_number(self, value):

        if value <= 0:
            raise serializers.ValidationError(
                "Ward number must be greater than zero."
            )

        return value


class FamilyMemberSerializer(serializers.ModelSerializer):
    family_name = serializers.CharField(
        source="family.house_name",
        read_only=True,
    )

    relationship_display = serializers.CharField(

        source="get_relationship_display",

        read_only=True,

    )

    gender_display = serializers.CharField(

        source="get_gender_display",

        read_only=True,

    )

    class Meta:
        model = FamilyMember
        fields = (

            "id",

            "family",

            "family_name",

            "first_name",

            "last_name",

            "baptism_name",

            "gender",

            "gender_display",

            "relationship",

            "relationship_display",

            "date_of_birth",

            "phone_number",

            "email",

            "occupation",

            "photo",

            "is_family_head",

            "is_active",

            "created_at",

            "updated_at",

        )

    def validate_first_name(self, value):
        value = value.strip()

        if len(value) < 2:
            raise serializers.ValidationError(
                "First name must contain at least 2 characters."
            )

        return value

    def validate_last_name(self, value):
        return value.strip()

    def validate_email(self, value):
        return value.strip().lower()

    def validate(self, attrs):

        family = attrs.get(
            "family",
            getattr(self.instance, "family", None)
        )

        is_family_head = attrs.get(
            "is_family_head",
            getattr(self.instance, "is_family_head", False)
        )

        if family and is_family_head:

            queryset = FamilyMember.objects.filter(
                family=family,
                is_family_head=True,
            )

            if self.instance:
                queryset = queryset.exclude(
                    pk=self.instance.pk
                )

            if queryset.exists():
                raise serializers.ValidationError(
                    {
                        "is_family_head": (
                            "Only one family head is allowed per family."
                        )
                    }
                )

        return attrs