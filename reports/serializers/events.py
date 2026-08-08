from rest_framework import serializers
from events.models import Event
from django.utils import timezone


class EventReportSerializer(serializers.ModelSerializer):
    """
    Serializer for Event reports.
    """

    family_unit = serializers.CharField(
        source="family_unit.family_unit_name",
        read_only=True,
    )
    event_status = serializers.SerializerMethodField()

    class Meta:
        model = Event

        fields = (
            "id",
            "title",
            "description",
            "event_type",
            "event_status",
            "family_unit",
            "venue",
            "start_datetime",
            "end_datetime",
            "is_public",
            "is_featured",
            "is_active",
            "created_at",
            "updated_at",
        )

        read_only_fields = fields

    def get_event_status(self, obj):
        now = timezone.now()

        if obj.start_datetime > now:
            return "UPCOMING"

        if obj.start_datetime <= now <= obj.end_datetime:
            return "ONGOING"

        return "COMPLETED"