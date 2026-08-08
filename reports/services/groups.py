from django.db.models import Count, Prefetch, Q
from parish_groups.models import ParishGroup, ParishGroupMember


class GroupReportService:
    """
    Business logic for Parish Group reports.

    This service contains only ORM/business logic.
    Views must never perform database queries.
    """

    @staticmethod
    def get_group_directory(search=None):
        """Returns all active parish groups."""

        queryset = (
            ParishGroup.objects
            .filter(is_active=True)
            .select_related("leader")
            .prefetch_related(
                Prefetch(
                    "members",
                    queryset=ParishGroupMember.objects.filter(
                        is_active=True,
                    ).select_related("member"),
                )
            )
            .order_by("name")
        )
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset

    @staticmethod
    def get_group_members_report(search=None, group=None):
        """Returns all active parish group memberships."""

        queryset = (
            ParishGroupMember.objects
            .filter(
                is_active=True,
                group__is_active=True,
            )
            .select_related(
                "group",
                "member",
            )
            .order_by(
                "group__name",
                "member__first_name",
                "member__last_name",
            )
        )
        if group:
            queryset = queryset.filter(group_id=group)
        if search:
            queryset = queryset.filter(
                Q(member__first_name__icontains=search) |
                Q(member__last_name__icontains=search) |
                Q(group__name__icontains=search)
            )
        return queryset

    @staticmethod
    def get_group_leaders_report(search=None):
        """Returns all active parish groups with their leaders."""

        queryset = (
            ParishGroup.objects
            .filter(is_active=True)
            .select_related("leader")
            .order_by("name")
        )
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(leader__first_name__icontains=search) |
                Q(leader__last_name__icontains=search)
            )
        return queryset

    @staticmethod
    def get_group_statistics_report(search=None):
        """Returns group statistics with active member counts."""

        queryset = (
            ParishGroup.objects
            .filter(is_active=True)
            .select_related("leader")
            .annotate(
                total_members=Count(
                    "members",
                    filter=Q(members__is_active=True),
                    distinct=True,
                ),
            )
            .order_by("name")
        )
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset
    