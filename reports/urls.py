from django.urls import path

from reports.views import (
    DashboardReportAPIView,
)
from reports.views.family import (
    FamilyDirectoryReportAPIView,
    FamilyHeadReportAPIView,
    FamilyMemberReportAPIView,
    FamilyUnitReportAPIView,
)
from reports.views.groups import (
    GroupDirectoryReportAPIView,
    GroupLeaderReportAPIView,
    GroupMemberReportAPIView,
    GroupStatisticsReportAPIView,
)
from reports.views.events import EventReportAPIView
from reports.views.notices import NoticeReportAPIView
from reports.views.users import (
    ActiveSessionsReportAPIView,
    DisabledAccountsReportAPIView,
    InvitationHistoryReportAPIView,
    LoginHistoryReportAPIView,
    PermissionAuditReportAPIView,
    RecentUsersReportAPIView,
)

# Staff Reports
from reports.views.staff import StaffReportAPIView
from reports.views.export import ReportExportAPIView

app_name = "reports"

urlpatterns = [
    path(
        "dashboard/",
        DashboardReportAPIView.as_view(),
        name="dashboard-report",
    ),
    path(
        "families/directory/",
        FamilyDirectoryReportAPIView.as_view(),
        name="family-directory-report",
    ),

    path(
        "families/unit-wise/",
        FamilyUnitReportAPIView.as_view(),
        name="family-unit-report",
    ),
    path(
        "families/heads/",
        FamilyHeadReportAPIView.as_view(),
        name="family-heads-report",
    ),
    path(
        "families/members/",
        FamilyMemberReportAPIView.as_view(),
        name="family-members-report",
    ),

    # Group Reports
    path(
        "groups/directory/",
        GroupDirectoryReportAPIView.as_view(),
        name="group-directory-report",
    ),
    path(
        "groups/members/",
        GroupMemberReportAPIView.as_view(),
        name="group-members-report",
    ),
    path(
        "groups/leaders/",
        GroupLeaderReportAPIView.as_view(),
        name="group-leaders-report",
    ),
    path(
        "groups/statistics/",
        GroupStatisticsReportAPIView.as_view(),
        name="group-statistics-report",
    ),

    ## EVENTS REPORTS

    path(
        "events/",
        EventReportAPIView.as_view(),
        name="event-report",
    ),

    # Notice Reports
    path(
        "notices/",
        NoticeReportAPIView.as_view(),
        name="notice-report",
    ),

    # User & Security Reports
    path(
        "users/login-history/",
        LoginHistoryReportAPIView.as_view(),
        name="login-history-report",
    ),
    path(
        "users/invitations/",
        InvitationHistoryReportAPIView.as_view(),
        name="invitation-history-report",
    ),
    path(
        "users/recent/",
        RecentUsersReportAPIView.as_view(),
        name="recent-users-report",
    ),
    path(
        "users/disabled/",
        DisabledAccountsReportAPIView.as_view(),
        name="disabled-accounts-report",
    ),
    path(
        "users/sessions/",
        ActiveSessionsReportAPIView.as_view(),
        name="active-sessions-report",
    ),
    path(
        "users/permission-audit/",
        PermissionAuditReportAPIView.as_view(),
        name="permission-audit-report",
    ),

    # Staff Reports
    path(
        "staff/",
        StaffReportAPIView.as_view(),
        name="staff-report",
    ),
    # Export Reports (SUPERADMIN only)
    path(
        "export/",
        ReportExportAPIView.as_view(),
        name="report-export",
    ),

    
]