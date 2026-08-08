from django.db import models
from rest_framework import serializers


class ReportExportRequestSerializer(serializers.Serializer):
    """
    Validates export requests.
    """

    class ReportChoices(models.TextChoices):

        FAMILY_DIRECTORY = "family-directory"
        FAMILY_UNIT_WISE = "family-unit-wise"
        FAMILY_HEADS = "family-heads"
        FAMILY_MEMBERS = "family-members"

        GROUP_DIRECTORY = "group-directory"
        GROUP_MEMBERS = "group-members"
        GROUP_LEADERS = "group-leaders"
        GROUP_STATISTICS = "group-statistics"

        EVENTS = "events"
        NOTICES = "notices"

        LOGIN_HISTORY = "login-history"
        INVITATIONS = "invitations"
        RECENT_USERS = "recent-users"
        DISABLED_USERS = "disabled-users"
        PERMISSION_AUDIT = "permission-audit"
        SESSIONS = "sessions"

        STAFF = "staff"

    class FormatChoices(models.TextChoices):
        CSV = "csv"
        XLSX = "xlsx"
        PDF = "pdf"

    report = serializers.ChoiceField(choices=ReportChoices.choices)
    format = serializers.ChoiceField(choices=FormatChoices.choices)

    filters = serializers.DictField(
        child=serializers.CharField(allow_blank=True),
        required=False,
        default=dict,
    )

    def validate_filters(self, value):
        return value or {}