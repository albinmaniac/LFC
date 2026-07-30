from django.utils import timezone
from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from lfc_project.pagination import StandardPagination

from accounts.permissions import (
    CanManageEvents,
    IsSuperAdmin,
    has_permission,
)
from parish.models import UserPermission
from events.models import Event,Feast

from .serializers import (
    EventSerializer,
    FeastSerializer,
    CalendarItemSerializer,
)


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

class FeaturedEventListAPIView(generics.ListAPIView):
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
                end_datetime__gte=timezone.now(),
            )
            .order_by("start_datetime")
        )


class UpcomingEventListAPIView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return (
            Event.objects
            .select_related("family_unit")
            .filter(
                is_active=True,
                is_public=True,
                end_datetime__gte=timezone.now(),
            )
            .order_by("start_datetime")
        )


    
class FeastListCreateAPIView(
        generics.ListCreateAPIView
    ):

    serializer_class = FeastSerializer
    pagination_class = StandardPagination

    filter_backends = [
        SearchFilter,
        OrderingFilter,
    ]

    search_fields = [
        "title",
        "description",
    ]

    ordering_fields = [
        "feast_date",
        "created_at",
        "title",
    ]

    ordering = [
        "feast_date",
    ]

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [
            IsAuthenticated(),
            CanManageEvents(),
        ]

    def get_queryset(self):
        queryset = Feast.objects.all()

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
            )

        # Filters
        featured = self.request.query_params.get("featured")
        active = self.request.query_params.get("active")
        month = self.request.query_params.get("month")
        year = self.request.query_params.get("year")

        if featured == "true":
            queryset = queryset.filter(is_featured=True)

        if is_admin_view:
            if active == "true":
                queryset = queryset.filter(is_active=True)
            elif active == "false":
                queryset = queryset.filter(is_active=False)
        # For non-admins, only active/public already filtered above

        if month:
            try:
                month = int(month)
                queryset = queryset.filter(feast_date__month=month)
            except ValueError:
                pass
        if year:
            try:
                year = int(year)
                queryset = queryset.filter(feast_date__year=year)
            except ValueError:
                pass

        return queryset


class FeastRetrieveUpdateDestroyAPIView(
        generics.RetrieveUpdateDestroyAPIView
    ):

    serializer_class = FeastSerializer

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
        queryset = Feast.objects.all()
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
            )
        return queryset


class FeaturedFeastListAPIView(generics.ListAPIView):
    serializer_class = FeastSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return (
            Feast.objects
            .filter(
                is_active=True,
                is_public=True,
                is_featured=True,
            )
            .order_by("feast_date")
        )

class CalendarAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        month = request.query_params.get("month")
        year = request.query_params.get("year")

        events = (
            Event.objects
            .select_related("family_unit")
            .filter(
                is_active=True,
                is_public=True,
            )
        )

        feasts = Feast.objects.filter(
            is_active=True,
            is_public=True,
        )

        try:
            if month:
                month = int(month)
                if not 1 <= month <= 12:
                    return Response(
                        {"detail": "Month must be between 1 and 12."},
                        status=400,
                    )
                events = events.filter(start_datetime__month=month)
                events = events.filter(start_datetime__year=year)

                feasts = feasts.filter(feast_date__month=month)
                feasts = feasts.filter(feast_date__year=year)

            if year:
                year = int(year)
                if year < 1900 or year > 9999:
                    return Response(
                        {"detail": "Invalid year."},
                        status=400,
                    )
                events = events.filter(start_datetime__year=year)
                feasts = feasts.filter(feast_date__year=year)

        except ValueError:
            return Response(
                {"detail": "Month and year must be integers."},
                status=400,
            )

        calendar_items = [
            {
                "type": "event",
                "id": event.id,
                "title": event.title,
                "date": event.start_datetime.date(),
                "is_featured": event.is_featured,
                "url": f"/api/events/{event.id}/",
            }
            for event in events
        ]

        calendar_items.extend([
            {
                "type": "feast",
                "id": feast.id,
                "title": feast.title,
                "date": feast.feast_date,
                "is_featured": feast.is_featured,
                "url": f"/api/events/feasts/{feast.id}/",
            }
            for feast in feasts
        ])

        calendar_items.sort(key=lambda item: (item["date"], item["type"], item["title"]))

        serializer = CalendarItemSerializer(calendar_items, many=True)
        return Response(serializer.data)

    