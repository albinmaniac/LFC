
from django.utils import timezone
from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from lfc_project.pagination import StandardPagination

from accounts.permissions import (
    CanManageNotices,
    IsSuperAdmin,
    has_permission,
)

from .models import Notice
from .serializers import NoticeSerializer
from parish.models import UserPermission

class NoticeListCreateAPIView(generics.ListCreateAPIView):
    # ...existing serializer_class, pagination_class, filter_backends, search_fields...
    pagination_class = StandardPagination
    serializer_class = NoticeSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["title", "content"]

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), CanManageNotices()]

    def get_queryset(self):
        queryset = Notice.objects.all()  # adjust to match your actual base queryset

        user = self.request.user
        is_admin_view = (
            self.request.method == "GET"
            and user.is_authenticated
            and has_permission(user, UserPermission.PermissionChoices.MANAGE_NOTICES)
        )

        if self.request.method == "GET" and not is_admin_view:
            queryset = queryset.filter(is_active=True, is_public=True)

        notice_type = self.request.query_params.get("notice_type")
        active = self.request.query_params.get("active")

        if notice_type:
            queryset = queryset.filter(notice_type=notice_type)
        if is_admin_view and active == "true":
            queryset = queryset.filter(is_active=True)
        elif is_admin_view and active == "false":
            queryset = queryset.filter(is_active=False)

        return queryset

class NoticeRetrieveUpdateDestroyAPIView(
    generics.RetrieveUpdateDestroyAPIView
):

    serializer_class = NoticeSerializer

    def get_permissions(self):

        if self.request.method == "GET":
            return [AllowAny()]

        if self.request.method == "DELETE":
            return [
                IsAuthenticated(),
                IsSuperAdmin(),
            ]

        return [
            IsAuthenticated(),
            CanManageNotices(),
        ]

    def get_queryset(self):

        queryset = Notice.objects.all()

        if self.request.method == "GET":
            queryset = queryset.filter(
                is_active=True,
                is_public=True,
            )

            queryset = queryset.exclude(
                expiry_date__isnull=False,
                expiry_date__lt=timezone.now(),
            )

        return queryset


class FeaturedNoticeListAPIView(
    generics.ListAPIView
):

    serializer_class = NoticeSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):

        return (
            Notice.objects
            .filter(
                is_active=True,
                is_public=True,
                is_featured=True,
            )
            .exclude(
                expiry_date__isnull=False,
                expiry_date__lt=timezone.now(),
            )
            .order_by("-publish_date")
        )


class ActiveNoticeListAPIView(
    generics.ListAPIView
):

    serializer_class = NoticeSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):

        return (
            Notice.objects
            .filter(
                is_active=True,
                is_public=True,
            )
            .exclude(
                expiry_date__isnull=False,
                expiry_date__lt=timezone.now(),
            )
            .order_by("-publish_date")
        )

