
from django.db.models import Q


from staffs.models import Staff


class StaffReportService:
    """
    Business logic for Staff reports.

    This service contains only ORM/business logic.
    Views must never perform database queries.
    """

    @staticmethod
    def get_staff_report(*, designation=None, status=None, search=None):
        """Returns staff with optional designation, status, and search filters."""

        queryset = Staff.objects.all()
        queryset = queryset.filter(is_active=True)
        queryset = queryset.order_by(
            "designation",
            "name",
        )

        if designation:
            queryset = queryset.filter(designation=designation)

        if status:
            queryset = queryset.filter(status=status)

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search)
                | Q(email__icontains=search)
                | Q(phone_number__icontains=search)
                | Q(designation__icontains=search)
            )

        return queryset

    @staticmethod
    def get_active_staff():
        """Returns active staff members."""

        return (
            Staff.objects
            .filter(status="ACTIVE", is_active=True)
            .order_by(
                "designation",
                "name",
            )
        )

    @staticmethod
    def get_retired_staff():
        """Returns retired staff members."""

        return (
            Staff.objects
            .filter(status="RETIRED", is_active=True)
            .order_by(
                "designation",
                "name",
            )
        )