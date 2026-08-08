from django.db.models import Prefetch, Q
from families.models import Family, FamilyMember, FamilyUnit


class FamilyReportService:
    """
    Business logic for Family reports.

    This service must contain only business logic.
    Views should never perform ORM queries.
    """

    @staticmethod
    def get_family_directory(search=None, family_unit=None, status=None):
        """
        Returns all active families for the Family Directory report.
        """

        queryset = (
            Family.objects
            .select_related("family_unit")
            .prefetch_related(
                Prefetch(
                    "members",
                    queryset=FamilyMember.objects.filter(is_active=True).order_by("first_name", "last_name"),
                )
            )
            .order_by(
                "family_unit__family_unit_name",
                "house_name",
            )
        )

        if status == "active":
            queryset = queryset.filter(is_active=True)
        elif status == "inactive":
            queryset = queryset.filter(is_active=False)

        if family_unit is not None:
            queryset = queryset.filter(family_unit_id=family_unit)

        if search:
            queryset = queryset.filter(house_name__icontains=search)

        return queryset

    @staticmethod
    def get_family_unit_report(search=None, status=None):
        """
        Returns the Family Unit report with aggregated counts.
        """

        from django.db.models import Count

        queryset = (
            FamilyUnit.objects
            .select_related(
                "president",
                "secretary",
            )
            .annotate(
                total_families=Count(
                    "families",
                    filter=Q(families__is_active=True),
                    distinct=True,
                ),
                total_members=Count(
                    "families__members",
                    filter=Q(
                        families__is_active=True,
                        families__members__is_active=True,
                    ),
                    distinct=True,
                ),
            )
            .order_by("family_unit_name")
        )

        if status == "active":
            queryset = queryset.filter(is_active=True)
        elif status == "inactive":
            queryset = queryset.filter(is_active=False)

        if search:
            queryset = queryset.filter(family_unit_name__icontains=search)

        return queryset

    @staticmethod
    def get_family_heads_report(search=None, family_unit=None, status=None):
        """
        Returns all active family heads.
        """

        queryset = (
            FamilyMember.objects
            .filter(
                is_family_head=True,
            )
            .select_related(
                "family",
                "family__family_unit",
            )
            .order_by(
                "family__family_unit__family_unit_name",
                "family__house_name",
                "first_name",
            )
        )

        if status == "active":
            queryset = queryset.filter(is_active=True, family__is_active=True)
        elif status == "inactive":
            queryset = queryset.filter(Q(is_active=False) | Q(family__is_active=False))

        if family_unit is not None:
            queryset = queryset.filter(family__family_unit_id=family_unit)

        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) | Q(last_name__icontains=search)
            )

        return queryset

    @staticmethod
    def get_family_members_report(search=None, family_unit=None, status=None):
        """
        Returns all active family members.
        """

        queryset = (
            FamilyMember.objects
            .select_related(
                "family",
                "family__family_unit",
            )
            .order_by(
                "family__family_unit__family_unit_name",
                "family__house_name",
                "first_name",
                "last_name",
            )
        )

        if status == "active":
            queryset = queryset.filter(is_active=True, family__is_active=True)
        elif status == "inactive":
            queryset = queryset.filter(Q(is_active=False) | Q(family__is_active=False))

        if family_unit is not None:
            queryset = queryset.filter(family__family_unit_id=family_unit)

        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) | Q(last_name__icontains=search)
            )

        return queryset
