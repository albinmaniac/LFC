from rest_framework import serializers


class DashboardReportSerializer(serializers.Serializer):
    """
    Serializer for dashboard summary statistics.
    """

    total_families = serializers.IntegerField(
        read_only=True,
        min_value=0,
    )

    total_family_members = serializers.IntegerField(
        read_only=True,
        min_value=0,
    )

    total_family_units = serializers.IntegerField(
        read_only=True,
        min_value=0,
    )

    total_parish_groups = serializers.IntegerField(
        read_only=True,
        min_value=0,
    )

    active_users = serializers.IntegerField(
        read_only=True,
        min_value=0,
    )

    pending_invitations = serializers.IntegerField(
        read_only=True,
        min_value=0,
    )

    total_events = serializers.IntegerField(
        read_only=True,
        min_value=0,
    )

    total_notices = serializers.IntegerField(
        read_only=True,
        min_value=0,
    )
    