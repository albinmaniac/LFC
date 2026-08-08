

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import CanViewReports
from reports.serializers.groups import (
    GroupDirectoryReportSerializer,
    GroupLeaderReportSerializer,
    GroupMemberReportSerializer,
    GroupStatisticsReportSerializer,
)
from reports.services.groups import GroupReportService


class GroupDirectoryReportAPIView(APIView):
    """Returns the Parish Group directory report."""

    permission_classes = [CanViewReports]

    def get(self, request):
        queryset = GroupReportService.get_group_directory()
        serializer = GroupDirectoryReportSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GroupMemberReportAPIView(APIView):
    """Returns the Parish Group members report."""

    permission_classes = [CanViewReports]

    def get(self, request):
        queryset = GroupReportService.get_group_members_report()
        serializer = GroupMemberReportSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GroupLeaderReportAPIView(APIView):
    """Returns the Parish Group leaders report."""

    permission_classes = [CanViewReports]

    def get(self, request):
        queryset = GroupReportService.get_group_leaders_report()
        serializer = GroupLeaderReportSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GroupStatisticsReportAPIView(APIView):
    """Returns the Parish Group statistics report."""

    permission_classes = [CanViewReports]

    def get(self, request):
        queryset = GroupReportService.get_group_statistics_report()
        serializer = GroupStatisticsReportSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)