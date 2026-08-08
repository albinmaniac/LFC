from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsSuperAdmin
from reports.serializers.export import ReportExportRequestSerializer
from reports.services.exports import ReportExportService


class ReportExportAPIView(APIView):
    """
    Export reports as CSV, XLSX, or PDF.

    Access: SUPERADMIN only.
    """

    permission_classes = [IsSuperAdmin]

    def post(self, request):
        serializer = ReportExportRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        report = serializer.validated_data["report"]
        export_format = serializer.validated_data["format"]
        filters = serializer.validated_data.get("filters", {})

        try:
            queryset = ReportExportService.get_queryset(
                report=report,
                filters=filters,
            )
        except ValueError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            headers, rows = ReportExportService.build_export_data(
                report=report,
                queryset=queryset,
            )
        except ValueError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if export_format == "csv":
            content = ReportExportService.export_csv(headers, rows)
            content_type = "text/csv"
            extension = "csv"
        elif export_format == "xlsx":
            content = ReportExportService.export_excel(headers, rows)
            content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            extension = "xlsx"
        else:
            content = ReportExportService.export_pdf(headers, rows)
            content_type = "application/pdf"
            extension = "pdf"

        response = HttpResponse(content, content_type=content_type)
        response["Content-Disposition"] = (
            f'attachment; filename="{report}.{extension}"'
        )
        return response