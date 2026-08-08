


from django.db.models import Q
from django.utils import timezone

from events.models import Event


class EventReportService:
    """
    Business logic for Event reports.

    This service contains only ORM/business logic.
    Views must never perform database queries.
    """

    @staticmethod
    def get_events_report(
        *,
        year=None,
        month=None,
        date=None,
        search=None,
    ):
        """
        Returns active events with optional date filters.
        """

        queryset = (
            Event.objects
            .select_related("family_unit")
            .order_by("-start_datetime")
        )

        if year:
            queryset = queryset.filter(start_datetime__year=year)

        if month:
            queryset = queryset.filter(start_datetime__month=month)

        if date:
            queryset = queryset.filter(start_datetime__date=date)

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search)
                | Q(description__icontains=search)
                | Q(venue__icontains=search)
            )

        return queryset

    @staticmethod
    def get_today_events():
        """Returns today's active events."""

        today = timezone.localdate()

        return (
            Event.objects
            .filter(
                is_active=True,
                start_datetime__date=today,
            )
            .select_related("family_unit")
            .order_by("start_datetime")
        )