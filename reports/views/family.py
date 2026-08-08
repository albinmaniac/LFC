from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import CanViewReports
from reports.serializers.family import (
    FamilyDirectoryReportSerializer,
    FamilyHeadReportSerializer,
    FamilyMemberReportSerializer,
    FamilyUnitReportSerializer,
)
from reports.services.family import FamilyReportService


class FamilyDirectoryReportAPIView(APIView):
    """
    Returns the Family Directory report.

    Business logic is delegated to FamilyReportService.
    This view should remain free of ORM queries.
    """

    permission_classes = [
        CanViewReports,
    ]

    def get(self, request):
        families = FamilyReportService.get_family_directory()

        serializer = FamilyDirectoryReportSerializer(
            families,
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class FamilyUnitReportAPIView(APIView):
    """
    Returns the Family Unit report.

    Business logic is delegated to FamilyReportService.
    """

    permission_classes = [
        CanViewReports,
    ]

    def get(self, request):
        queryset = FamilyReportService.get_family_unit_report()

        serializer = FamilyUnitReportSerializer(
            queryset,
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class FamilyHeadReportAPIView(APIView):
    """Returns the Family Heads report."""

    permission_classes = [CanViewReports]

    def get(self, request):
        queryset = FamilyReportService.get_family_heads_report()

        serializer = FamilyHeadReportSerializer(
            queryset,
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class FamilyMemberReportAPIView(APIView):
    """Returns the Family Members report."""

    permission_classes = [CanViewReports]

    def get(self, request):
        queryset = FamilyReportService.get_family_members_report()

        serializer = FamilyMemberReportSerializer(
            queryset,
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
