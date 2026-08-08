
from django.db.models import Q


from notices.models import Notice


class NoticeReportService:
    """
    Business logic for Notice reports.

    This service contains only ORM/business logic.
    Views must never perform database queries.
    """

    @staticmethod
    def get_notices_report(
        *,
        year=None,
        month=None,
        date=None,
        search=None,
    ):
        """
        Returns active notices with optional search and date filters.
        """

        queryset = (
            Notice.objects
            .filter(is_active=True)
            .order_by("-publish_date")
        )

        if year:
            queryset = queryset.filter(publish_date__year=year)

        if month:
            queryset = queryset.filter(publish_date__month=month)

        if date:
            queryset = queryset.filter(publish_date__date=date)

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search)
                | Q(content__icontains=search)
            )

        return queryset

    @staticmethod
    def get_featured_notices():
        """Returns all active featured notices."""

        return (
            Notice.objects
            .filter(
                is_active=True,
                is_featured=True,
            )
            .order_by("-publish_date")
        )