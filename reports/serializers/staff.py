

from rest_framework import serializers

from staffs.models import Staff


class StaffReportSerializer(serializers.ModelSerializer):
    """
    Serializer for Staff reports.
    """

    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Staff

        fields = (
            "id",
            "name",
            "designation",
            "email",
            "phone_number",
            "photo_url",
            "bio",
            "start_date",
            "end_date",
            "show_email_publicly",
            "show_phone_publicly",
            "status",
            "is_active",
            "created_at",
            "updated_at",
        )

        read_only_fields = fields

    def get_photo_url(self, obj):
        if not obj.photo:
            return None
        return obj.photo.url