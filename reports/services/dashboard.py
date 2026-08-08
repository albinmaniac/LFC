"""
Business logic for report generation.

Views must never contain ORM queries.
All report calculations belong in this module.
"""

from typing import Dict

from accounts.models import Invitation, User
from events.models import Event
from families.models import Family, FamilyMember, FamilyUnit
from notices.models import Notice
from parish_groups.models import ParishGroup


class DashboardReportService:
    """
    Service responsible for generating dashboard report data.

    Note: This service must remain free of HTTP/DRF concerns and should only contain business logic.
    """

    @staticmethod
    def get_dashboard_summary() -> Dict[str, int]:
        """
        Returns dashboard summary statistics.
        """

        total_families = Family.objects.filter(is_active=True).count()
        total_family_members = FamilyMember.objects.filter(is_active=True).count()
        total_family_units = FamilyUnit.objects.filter(is_active=True).count()
        total_parish_groups = ParishGroup.objects.filter(is_active=True).count()
        active_users = User.objects.filter(is_active=True).count()
        pending_invitations = Invitation.objects.filter(status=Invitation.Status.PENDING).count()
        total_events = Event.objects.filter(is_active=True).count()
        total_notices = Notice.objects.filter(is_active=True).count()

        return {
            "total_families": total_families,
            "total_family_members": total_family_members,
            "total_family_units": total_family_units,
            "total_parish_groups": total_parish_groups,
            "active_users": active_users,
            "pending_invitations": pending_invitations,
            "total_events": total_events,
            "total_notices": total_notices,
        }

    