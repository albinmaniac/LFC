from rest_framework import serializers
from parish_groups.models import ParishGroup, ParishGroupMember


class GroupDirectoryReportSerializer(serializers.ModelSerializer):
    """Serializer for the Parish Group directory report."""

    leader_name = serializers.SerializerMethodField()
    total_members = serializers.SerializerMethodField()

    class Meta:
        model = ParishGroup
        fields = (
            "id",
            "name",
            "description",
            "leader_name",
            "total_members",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields

    def get_leader_name(self, obj):
        if not obj.leader:
            return None
        return f"{obj.leader.first_name} {obj.leader.last_name}".strip()

    def get_total_members(self, obj):
        return obj.members.filter(is_active=True).count()


class GroupMemberReportSerializer(serializers.ModelSerializer):
    """Serializer for Parish Group members report."""

    group_name = serializers.CharField(source="group.name", read_only=True)
    member_name = serializers.SerializerMethodField()

    class Meta:
        model = ParishGroupMember
        fields = (
            "id",
            "group_name",
            "member_name",
            "is_active",
            "created_at",
        )
        read_only_fields = fields

    def get_member_name(self, obj):
        member = obj.member
        return f"{member.first_name} {member.last_name}".strip()


class GroupLeaderReportSerializer(serializers.ModelSerializer):
    """Serializer for Parish Group leaders."""

    leader_name = serializers.SerializerMethodField()

    class Meta:
        model = ParishGroup
        fields = (
            "id",
            "name",
            "leader_name",
            "phone_number",
            "is_active",
        )
        read_only_fields = fields

    def get_leader_name(self, obj):
        if not obj.leader:
            return None
        return f"{obj.leader.first_name} {obj.leader.last_name}".strip()


class GroupStatisticsReportSerializer(serializers.ModelSerializer):
    """Serializer for Parish Group statistics."""

    leader_name = serializers.SerializerMethodField()
    total_members = serializers.IntegerField(read_only=True)

    class Meta:
        model = ParishGroup
        fields = (
            "id",
            "name",
            "leader_name",
            "total_members",
            "is_active",
        )
        read_only_fields = fields

    def get_leader_name(self, obj):
        if not obj.leader:
            return None
        return f"{obj.leader.first_name} {obj.leader.last_name}".strip()