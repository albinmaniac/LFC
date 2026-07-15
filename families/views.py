from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.filters import SearchFilter
from lfc_project.pagination import StandardPagination

from accounts.permissions import (
        CanManageFamilies,
        CanManageFamilyMembers,
        CanManageFamilyUnits,
        IsSuperAdmin,
    )

from .models import Family, FamilyMember, FamilyUnit
from .serializers import (
        FamilyMemberSerializer,
        FamilySerializer,
        FamilyUnitSerializer,
    )


class FamilyUnitListCreateAPIView(
        generics.ListCreateAPIView
):
    queryset = (

        FamilyUnit.objects

        .select_related(

            "president",

            "secretary",

        )

        .filter(

            is_active=True

        )

        .order_by(

            "family_unit_name"

        )

    )

    filter_backends = [SearchFilter]

    search_fields = [
        "family_unit_name",
        "saint",
    ]
    serializer_class = FamilyUnitSerializer
    pagination_class = StandardPagination

    def get_permissions(self):
        if self.request.method == "POST":
            return [
                IsAuthenticated(),
                CanManageFamilyUnits(),
            ]

        return [AllowAny()]


class FamilyUnitRetrieveUpdateDestroyAPIView(
        generics.RetrieveUpdateDestroyAPIView
    ):
    queryset = (

        FamilyUnit.objects

        .select_related(

            "president",

            "secretary",

        )

        .filter(

            is_active=True

        )

    )
    serializer_class = FamilyUnitSerializer

    def get_permissions(self):
        if self.request.method == "DELETE":
            return [
                IsAuthenticated(),
                IsSuperAdmin(),
            ]

        if self.request.method in [
            "PUT",
            "PATCH",
        ]:
            return [
                IsAuthenticated(),
                CanManageFamilyUnits(),
            ]

        return [AllowAny()]


class FamilyListCreateAPIView(
        generics.ListCreateAPIView
    ):
    serializer_class = FamilySerializer

    filter_backends = [SearchFilter]

    search_fields = [
        "house_name",
        "phone_number",
        "email",
    ]
    pagination_class = StandardPagination

    def get_queryset(self):
        queryset = Family.objects.select_related(
            "family_unit"
        ).filter(
            is_active=True
        )

        family_unit = self.request.GET.get(
            "family_unit"
        )

        if family_unit:
            queryset = queryset.filter(
                family_unit_id=family_unit
            )

        return queryset.order_by(
            "house_name"
        )

    def get_permissions(self):
        if self.request.method == "GET":
            return [
                IsAuthenticated(),
            ]

        return [
            IsAuthenticated(),
            CanManageFamilies(),
        ]


class FamilyRetrieveUpdateDestroyAPIView(
        generics.RetrieveUpdateDestroyAPIView
    ):
    queryset = Family.objects.select_related(
        "family_unit"
    ).filter(
        is_active=True
    )
    serializer_class = FamilySerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [
                IsAuthenticated(),
            ]

        if self.request.method == "DELETE":
            return [
                IsAuthenticated(),
                IsSuperAdmin(),
            ]

        return [
            IsAuthenticated(),
            CanManageFamilies(),
        ]


class FamilyMemberListCreateAPIView(
        generics.ListCreateAPIView
    ):
    serializer_class = FamilyMemberSerializer

    filter_backends = [SearchFilter]

    search_fields = [
        "first_name",
        "last_name",
        "baptism_name",
        "phone_number",
        "email",
    ]
    pagination_class = StandardPagination

    def get_queryset(self):
        queryset = FamilyMember.objects.select_related(
            "family",
            "family__family_unit",
        ).filter(
            is_active=True
        )

        family = self.request.GET.get("family")

        if family:
            queryset = queryset.filter(
                family_id=family
            )

        return queryset.order_by(
            "first_name"
        )

    def get_permissions(self):
        if self.request.method == "GET":
            return [
                IsAuthenticated(),
            ]

        return [
            IsAuthenticated(),
            CanManageFamilyMembers(),
        ]


class FamilyMemberRetrieveUpdateDestroyAPIView(
        generics.RetrieveUpdateDestroyAPIView
    ):
    queryset = FamilyMember.objects.select_related(
        "family",
        "family__family_unit",
    ).filter(
        is_active=True
    )
    serializer_class = FamilyMemberSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [
                IsAuthenticated(),
            ]

        if self.request.method == "DELETE":
            return [
                IsAuthenticated(),
                IsSuperAdmin(),
            ]

        return [
            IsAuthenticated(),
            CanManageFamilyMembers(),
        ]
