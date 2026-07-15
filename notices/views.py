
from django.utils import timezone
from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from lfc_project.pagination import StandardPagination

from accounts.permissions import (
    CanManageNotices,
    IsSuperAdmin,
)

from .models import Notice
from .serializers import NoticeSerializer


class NoticeListCreateAPIView(
    generics.ListCreateAPIView
):

    serializer_class = NoticeSerializer
    pagination_class = StandardPagination
    filter_backends = [
        SearchFilter,
        OrderingFilter,
    ]

    search_fields = [
        "title",
        "content",
    ]

    ordering_fields = [
        "publish_date",
        "created_at",
        "title",
    ]

    ordering = [
        "-publish_date",
    ]

    def get_permissions(self):

        if self.request.method == "GET":
            return [AllowAny()]

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

        notice_type = self.request.query_params.get(
            "notice_type"
        )

        featured = self.request.query_params.get(
            "featured"
        )

        active = self.request.query_params.get(
            "active"
        )

        if notice_type:
            queryset = queryset.filter(
                notice_type=notice_type,
            )

        if featured == "true":
            queryset = queryset.filter(
                is_featured=True,
            )

        if active == "true":
            queryset = queryset.filter(
                is_active=True,
            )

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

