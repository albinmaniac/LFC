
from django.utils import timezone
from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from lfc_project.pagination import StandardPagination

from accounts.permissions import (
    CanManageEvents,
    IsSuperAdmin,
    has_permission,
)
from parish.models import UserPermission

from .models import Event
from .serializers import EventSerializer


class EventListCreateAPIView(
        generics.ListCreateAPIView
    ):

    serializer_class = EventSerializer
    pagination_class = StandardPagination

    filter_backends = [
        SearchFilter,
        OrderingFilter,
    ]

    search_fields = [
        "title",
        "venue",
        "description",
    ]

    ordering_fields = [
        "start_datetime",
        "created_at",
        "title",
    ]

    ordering = [
        "start_datetime",
    ]

    def get_permissions(self):

        if self.request.method == "GET":
            return [AllowAny()]

        return [
            IsAuthenticated(),
            CanManageEvents(),
        ]

    def get_queryset(self):
        queryset = Event.objects.select_related(
            "family_unit"
        )

        user = self.request.user
        is_admin_view = (
            self.request.method == "GET"
            and user.is_authenticated
            and (
                user.is_superuser
                or has_permission(user, UserPermission.PermissionChoices.MANAGE_EVENTS)
            )
        )

        if self.request.method == "GET" and not is_admin_view:
            queryset = queryset.filter(
                is_active=True,
                is_public=True,
                end_datetime__gte=timezone.now(),
            )

        event_type = self.request.query_params.get(
            "event_type"
        )

        family_unit = self.request.query_params.get(
            "family_unit"
        )

        featured = self.request.query_params.get(
            "featured"
        )

        upcoming = self.request.query_params.get(
            "upcoming"
        )

        if event_type:
            queryset = queryset.filter(
                event_type=event_type,
            )

        if family_unit:
            queryset = queryset.filter(
                family_unit_id=family_unit,
            )

        if featured == "true":
            queryset = queryset.filter(
                is_featured=True,
            )

        if upcoming == "true":
            queryset = queryset.filter(
                start_datetime__gte=timezone.now(),
            )

        # Admin active filter
        active = self.request.query_params.get("active")
        if is_admin_view and active == "true":
            queryset = queryset.filter(is_active=True)
        elif is_admin_view and active == "false":
            queryset = queryset.filter(is_active=False)

        return queryset


class EventRetrieveUpdateDestroyAPIView(
        generics.RetrieveUpdateDestroyAPIView
    ):

    serializer_class = EventSerializer

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
            CanManageEvents(),
        ]

    def get_queryset(self):
        queryset = Event.objects.select_related(
            "family_unit"
        )

        user = self.request.user
        is_admin_view = (
            self.request.method == "GET"
            and user.is_authenticated
            and (
                user.is_superuser
                or has_permission(user, UserPermission.PermissionChoices.MANAGE_EVENTS)
            )
        )

        if self.request.method == "GET" and not is_admin_view:
            return queryset.filter(
                is_active=True,
                is_public=True,
                end_datetime__gte=timezone.now(),
            )

        return queryset


class FeaturedEventListAPIView(
        generics.ListAPIView
    ):

    serializer_class = EventSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):

        return (
            Event.objects
            .select_related("family_unit")
            .filter(
                is_active=True,
                is_public=True,
                is_featured=True,
                start_datetime__gte=timezone.now(),
            )
            .order_by("start_datetime")
        )


class UpcomingEventListAPIView(
            generics.ListAPIView
        ):

    serializer_class = EventSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):

        return (
            Event.objects
            .select_related("family_unit")
            .filter(
                is_active=True,
                is_public=True,
                start_datetime__gte=timezone.now(),
            )
            .order_by("start_datetime")
        )


