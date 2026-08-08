import csv
from io import BytesIO, StringIO

from openpyxl import Workbook
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

from reports.serializers.events import EventReportSerializer
from reports.serializers.family import (
    FamilyDirectoryReportSerializer,
    FamilyHeadReportSerializer,
    FamilyMemberReportSerializer,
    FamilyUnitReportSerializer,
)
from reports.serializers.groups import (
    GroupDirectoryReportSerializer,
    GroupLeaderReportSerializer,
    GroupMemberReportSerializer,
    GroupStatisticsReportSerializer,
)
from reports.serializers.notices import NoticeReportSerializer
from reports.serializers.staff import StaffReportSerializer
from reports.serializers.users import (
    ActiveSessionReportSerializer,
    InvitationReportSerializer,
    LoginHistoryReportSerializer,
    PermissionAuditReportSerializer,
    RecentUserReportSerializer,
)
from reports.services.events import EventReportService
from reports.services.family import FamilyReportService
from reports.services.groups import GroupReportService
from reports.services.notices import NoticeReportService
from reports.services.staff import StaffReportService
from reports.services.users import UserReportService


class ReportExportService:
    """Generates CSV, XLSX and PDF exports using existing report services."""

    REPORT_MAP = {
        "family-directory": FamilyReportService.get_family_directory,
        "family-unit-wise": FamilyReportService.get_family_unit_report,
        "family-heads": FamilyReportService.get_family_heads_report,
        "family-members": FamilyReportService.get_family_members_report,
        "group-directory": GroupReportService.get_group_directory,
        "group-members": GroupReportService.get_group_members_report,
        "group-leaders": GroupReportService.get_group_leaders_report,
        "group-statistics": GroupReportService.get_group_statistics_report,
        "events": EventReportService.get_events_report,
        "notices": NoticeReportService.get_notices_report,
        "login-history": UserReportService.get_login_history,
        "invitations": UserReportService.get_invitation_history,
        "recent-users": UserReportService.get_recent_users,
        "disabled-users": UserReportService.get_disabled_accounts,
        "sessions": UserReportService.get_active_sessions,
        "permission-audit": UserReportService.get_permission_audit,
        "staff": StaffReportService.get_staff_report,
    }

    SERIALIZER_MAP = {
        "family-directory": FamilyDirectoryReportSerializer,
        "family-unit-wise": FamilyUnitReportSerializer,
        "family-heads": FamilyHeadReportSerializer,
        "family-members": FamilyMemberReportSerializer,
        "group-directory": GroupDirectoryReportSerializer,
        "group-members": GroupMemberReportSerializer,
        "group-leaders": GroupLeaderReportSerializer,
        "group-statistics": GroupStatisticsReportSerializer,
        "events": EventReportSerializer,
        "notices": NoticeReportSerializer,
        "login-history": LoginHistoryReportSerializer,
        "invitations": InvitationReportSerializer,
        "recent-users": RecentUserReportSerializer,
        "sessions": ActiveSessionReportSerializer,
        "permission-audit": PermissionAuditReportSerializer,
        "staff": StaffReportSerializer,
    }

    @classmethod
    def get_queryset(cls, report, filters=None):
        service = cls.REPORT_MAP.get(report)
        if service is None:
            raise ValueError(f"Unsupported report: {report}")

        filters = {
            key: value
            for key, value in (filters or {}).items()
            if value not in (None, "", [], {}, ())
        }

        # Each report service is responsible for applying the supported filters
        # (search, year, month, status, family_unit, etc.) before returning
        # the queryset used for export.
        return service(**filters)

    @classmethod
    def build_export_data(cls, report, queryset):
        serializer_class = cls.SERIALIZER_MAP.get(report)
        if serializer_class is None:
            raise ValueError(f"No serializer configured for report: {report}")

        data = serializer_class(queryset, many=True).data

        if not data:
            return [], []

        headers = [key.replace("_", " ").title() for key in data[0].keys()]
        rows = [list(item.values()) for item in data]
        return headers, rows

    @staticmethod
    def export_csv(headers, rows):
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(headers)
        writer.writerows(rows)
        return output.getvalue().encode("utf-8")

    @staticmethod
    def export_excel(headers, rows):
        wb = Workbook()
        ws = wb.active
        ws.append(headers)
        for row in rows:
            ws.append(row)
        stream = BytesIO()
        wb.save(stream)
        return stream.getvalue()

    @staticmethod
    def export_pdf(headers, rows):
        stream = BytesIO()
        doc = SimpleDocTemplate(stream, pagesize=landscape(letter))
        table = Table([headers, *rows])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ]))
        doc.build([table])
        return stream.getvalue()

    