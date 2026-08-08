



from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import CanViewReports
from reports.serializers.users import (
    ActiveSessionReportSerializer,
    InvitationReportSerializer,
    LoginHistoryReportSerializer,
    PermissionAuditReportSerializer,
    RecentUserReportSerializer,
)
from reports.services.users import UserReportService


class LoginHistoryReportAPIView(APIView):
    permission_classes = [CanViewReports]

    def get(self, request):
        queryset = UserReportService.get_login_history()
        serializer = LoginHistoryReportSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class InvitationHistoryReportAPIView(APIView):
    permission_classes = [CanViewReports]

    def get(self, request):
        queryset = UserReportService.get_invitation_history()
        serializer = InvitationReportSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RecentUsersReportAPIView(APIView):
    permission_classes = [CanViewReports]

    def get(self, request):
        queryset = UserReportService.get_recent_users()
        serializer = RecentUserReportSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DisabledAccountsReportAPIView(APIView):
    permission_classes = [CanViewReports]

    def get(self, request):
        queryset = UserReportService.get_disabled_accounts()
        serializer = RecentUserReportSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ActiveSessionsReportAPIView(APIView):
    permission_classes = [CanViewReports]

    def get(self, request):
        queryset = UserReportService.get_active_sessions()
        serializer = ActiveSessionReportSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PermissionAuditReportAPIView(APIView):
    permission_classes = [CanViewReports]

    def get(self, request):
        queryset = UserReportService.get_permission_audit()
        serializer = PermissionAuditReportSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    