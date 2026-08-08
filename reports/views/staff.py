

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import CanViewReports
from reports.serializers.staff import StaffReportSerializer
from reports.services.staff import StaffReportService


class StaffReportAPIView(APIView):
    """
    Returns the Staff report.

    Supports optional filtering using query parameters:
    - designation
    - status
    """

    permission_classes = [CanViewReports]

    def get(self, request):
        queryset = StaffReportService.get_staff_report(
            designation=request.query_params.get("designation"),
            status=request.query_params.get("status"),
        )

        serializer = StaffReportSerializer(
            queryset,
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )