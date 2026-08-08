from rest_framework import serializers

from notices.models import Notice


class NoticeReportSerializer(serializers.ModelSerializer):
    """
    Serializer for Notice reports.
    """

    class Meta:
        model = Notice
        fields = (
            "id",
            "title",
            "notice_type",
            "content",
            "publish_date",
            "expiry_date",
            "is_featured",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields