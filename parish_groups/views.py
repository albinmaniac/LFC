
from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from lfc_project.pagination import StandardPagination

from accounts.permissions import (
        CanManageGroups,
        IsSuperAdmin,
    )

from .models import (
        ParishGroup,
        ParishGroupMember,
    )

from .serializers import (
        ParishGroupSerializer,
        ParishGroupMemberSerializer,
    )


class ParishGroupListCreateAPIView(
        generics.ListCreateAPIView
    ):

    serializer_class = ParishGroupSerializer

    filter_backends = [
        SearchFilter,
        OrderingFilter,
    ]

    search_fields = [
        "name",
        "patron_saint",
    ]

    ordering_fields = [
        "name",
        "created_at",
    ]

    ordering = ["name"]

    def get_permissions(self):

        if self.request.method == "GET":
            return [AllowAny()]

        return [
            IsAuthenticated(),
            CanManageGroups(),
        ]

    def get_queryset(self):

        return ParishGroup.objects.select_related(
            "leader"
        ).filter(
            is_active=True
        )


class ParishGroupRetrieveUpdateDestroyAPIView(
        generics.RetrieveUpdateDestroyAPIView
    ):

    serializer_class = ParishGroupSerializer

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
            CanManageGroups(),
        ]

    def get_queryset(self):

        return ParishGroup.objects.select_related(
            "leader"
        ).filter(
            is_active=True
        )


class ParishGroupMemberListCreateAPIView(
        generics.ListCreateAPIView
    ):
    pagination_class = StandardPagination
    serializer_class = ParishGroupMemberSerializer

    filter_backends = [
        SearchFilter,
        OrderingFilter,
    ]

    search_fields = [
        "group__name",
        "member__first_name",
        "member__last_name",
        "member__baptism_name",
    ]

    ordering_fields = [
        "joined_date",
        "created_at",
    ]

    ordering = ["group"]

    def get_permissions(self):

        if self.request.method == "GET":
            return [AllowAny()]

        return [
            IsAuthenticated(),
            CanManageGroups(),
        ]

    def get_queryset(self):

        queryset = ParishGroupMember.objects.select_related(
            "group",
            "member",
        ).filter(
            is_active=True,
        )

        group_id = self.request.query_params.get(
            "group"
        )

        if group_id:
            queryset = queryset.filter(
                group_id=group_id
            )

        return queryset


class ParishGroupMemberRetrieveUpdateDestroyAPIView(
        generics.RetrieveUpdateDestroyAPIView
    ):

    serializer_class = ParishGroupMemberSerializer

    def get_permissions(self):

        if self.request.method == "DELETE":
            return [
                IsAuthenticated(),
                IsSuperAdmin(),
            ]

        return [
            IsAuthenticated(),
            CanManageGroups(),
        ]

    def get_queryset(self):

        return ParishGroupMember.objects.select_related(
            "group",
            "member",
        ).filter(
            is_active=True,
        )
