from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import CanViewReports
from reports.serializers import DashboardReportSerializer
from reports.services import DashboardReportService


class DashboardReportAPIView(APIView):
    """
    Returns dashboard summary statistics.
    """

    permission_classes = [
        CanViewReports,
    ]

    def get(self, request):

        summary = DashboardReportService.get_dashboard_summary()

        serializer = DashboardReportSerializer(summary)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

