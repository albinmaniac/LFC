

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import CanViewReports
from reports.serializers.events import EventReportSerializer
from reports.services.events import EventReportService


class EventReportAPIView(APIView):
    """
    Returns the Event report.

    Supports optional filtering using query parameters:
    - year
    - month
    - date (YYYY-MM-DD)
    """

    permission_classes = [CanViewReports]

    def get(self, request):
        queryset = EventReportService.get_events_report(
            year=request.query_params.get("year"),
            month=request.query_params.get("month"),
            date=request.query_params.get("date"),
        )

        serializer = EventReportSerializer(
            queryset,
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )