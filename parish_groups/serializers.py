from rest_framework import serializers

from .models import (
    ParishGroup,
    ParishGroupMember,
)


class ParishGroupSerializer(serializers.ModelSerializer):

    leader_name = serializers.SerializerMethodField()

    member_count = serializers.SerializerMethodField()

    class Meta:

        model = ParishGroup

        fields = (
            "id",
            "name",
            "description",
            "patron_saint",
            "photo",
            "leader",
            "leader_name",
            "phone_number",
            "member_count",
            "is_active",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
            "member_count",
        )

    def validate_name(self, value):

        value = value.strip()

        queryset = ParishGroup.objects.filter(
            name__iexact=value
        )

        if self.instance:
            queryset = queryset.exclude(
                pk=self.instance.pk
            )

        if queryset.exists():
            raise serializers.ValidationError(
                "A parish group with this name already exists."
            )

        return value

    def validate_phone_number(self, value):

        if value:

            value = value.strip()

            if not value.isdigit():
                raise serializers.ValidationError(
                    "Phone number must contain digits only."
                )

            if len(value) < 10 or len(value) > 15:
                raise serializers.ValidationError(
                    "Phone number must be between 10 and 15 digits."
                )

        return value

    def get_leader_name(self, obj):

        if obj.leader:
            return (
                f"{obj.leader.first_name} "
                f"{obj.leader.last_name}"
            ).strip()

        return None

    def get_member_count(self, obj):

        return obj.members.filter(
            is_active=True
        ).count()


class ParishGroupMemberSerializer(
        serializers.ModelSerializer
    ):

    group_name = serializers.CharField(
        source="group.name",
        read_only=True,
    )

    member_name = serializers.SerializerMethodField()
    member_photo = serializers.SerializerMethodField()

    class Meta:

        model = ParishGroupMember

        fields = (
            "id",
            "group",
            "group_name",
            "member",
            "member_name",
            "member_photo",
            "role",
            "joined_date",
            "is_active",
            "created_at",
        )

        read_only_fields = (
            "id",
            "created_at",
        )

    def validate(self, attrs):

        group = attrs.get(
            "group",
            getattr(
                self.instance,
                "group",
                None,
            ),
        )

        member = attrs.get(
            "member",
            getattr(
                self.instance,
                "member",
                None,
            ),
        )

        queryset = (
            ParishGroupMember.objects.filter(
                group=group,
                member=member,
            )
        )

        if self.instance:
            queryset = queryset.exclude(
                pk=self.instance.pk
            )

        if queryset.exists():
            raise serializers.ValidationError(
                {
                    "member":
                    "This member already belongs to this group."
                }
            )

        return attrs

    def get_member_name(self, obj):

        return (
            f"{obj.member.first_name} "
            f"{obj.member.last_name}"
        ).strip()
    
    def get_member_photo(self, obj):

        if obj.member and obj.member.photo:
            return obj.member.photo.url

        return None
    
    