from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.filters import SearchFilter
from lfc_project.pagination import StandardPagination

from accounts.permissions import (
    CanManageFamilies,
    CanManageFamilyMembers,
    CanManageFamilyUnits,
    IsSuperAdmin,
    has_permission,
)
from parish.models import UserPermission

from .models import Family, FamilyMember, FamilyUnit
from .serializers import (
    FamilyMemberSerializer,
    FamilySerializer,
    FamilyUnitSerializer,
)


class FamilyUnitListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = FamilyUnitSerializer
    pagination_class = StandardPagination
    filter_backends = [SearchFilter]
    search_fields = ["family_unit_name", "saint"]

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), CanManageFamilyUnits()]
        return [AllowAny()]

    def get_queryset(self):
        queryset = FamilyUnit.objects.select_related("president", "secretary")

        user = self.request.user
        is_admin_view = (
            self.request.method == "GET"
            and user.is_authenticated
            and has_permission(user, UserPermission.PermissionChoices.MANAGE_FAMILY_UNITS)
        )

        # Public/unauthenticated visitors and users without MANAGE_FAMILY_UNITS
        # only ever see active family units. Only users with that permission
        # (or SuperAdmin, via has_permission's own bypass) see everything.
        if self.request.method == "GET" and not is_admin_view:
            queryset = queryset.filter(is_active=True)

        active = self.request.query_params.get("active")
        if is_admin_view and active == "true":
            queryset = queryset.filter(is_active=True)
        elif is_admin_view and active == "false":
            queryset = queryset.filter(is_active=False)

        return queryset.order_by("family_unit_name")


class FamilyUnitRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FamilyUnitSerializer

    def get_permissions(self):
        if self.request.method == "DELETE":
            return [IsAuthenticated(), IsSuperAdmin()]
        if self.request.method in ["PUT", "PATCH"]:
            return [IsAuthenticated(), CanManageFamilyUnits()]
        return [AllowAny()]

    def get_queryset(self):
        queryset = FamilyUnit.objects.select_related("president", "secretary")

        user = self.request.user
        is_admin_view = (
            self.request.method == "GET"
            and user.is_authenticated
            and has_permission(user, UserPermission.PermissionChoices.MANAGE_FAMILY_UNITS)
        )

        if self.request.method == "GET" and not is_admin_view:
            return queryset.filter(is_active=True)

        return queryset


class FamilyListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = FamilySerializer
    filter_backends = [SearchFilter]
    search_fields = ["house_name", "phone_number", "email"]
    pagination_class = StandardPagination

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAuthenticated(), CanManageFamilies()]

    def get_queryset(self):
        queryset = Family.objects.select_related("family_unit")

        user = self.request.user
        is_admin_view = (
            self.request.method == "GET"
            and user.is_authenticated
            and has_permission(
                user,
                UserPermission.PermissionChoices.MANAGE_FAMILIES,
            )
        )

        if self.request.method == "GET" and not is_admin_view:
            queryset = queryset.filter(is_active=True)

        family_unit = self.request.query_params.get("family_unit")
        if family_unit:
            queryset = queryset.filter(family_unit_id=family_unit)

        active = self.request.query_params.get("active")
        if is_admin_view and active == "true":
            queryset = queryset.filter(is_active=True)
        elif is_admin_view and active == "false":
            queryset = queryset.filter(is_active=False)

        return queryset.order_by("house_name")


class FamilyRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FamilySerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        if self.request.method == "DELETE":
            return [IsAuthenticated(), IsSuperAdmin()]
        return [IsAuthenticated(), CanManageFamilies()]

    def get_queryset(self):
        queryset = Family.objects.select_related("family_unit")

        user = self.request.user
        is_admin_view = (
            self.request.method == "GET"
            and user.is_authenticated
            and has_permission(
                user,
                UserPermission.PermissionChoices.MANAGE_FAMILIES,
            )
        )

        if self.request.method == "GET" and not is_admin_view:
            return queryset.filter(is_active=True)

        return queryset


class FamilyMemberListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = FamilyMemberSerializer
    filter_backends = [SearchFilter]
    search_fields = ["first_name", "last_name", "baptism_name", "phone_number", "email"]
    pagination_class = StandardPagination

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAuthenticated(), CanManageFamilyMembers()]

    def get_queryset(self):
        queryset = FamilyMember.objects.select_related("family", "family__family_unit")

        user = self.request.user
        is_admin_view = (
            self.request.method == "GET"
            and user.is_authenticated
            and has_permission(
                user,
                UserPermission.PermissionChoices.MANAGE_FAMILY_MEMBERS,
            )
        )

        if self.request.method == "GET" and not is_admin_view:
            queryset = queryset.filter(is_active=True)

        family = self.request.query_params.get("family")
        if family:
            queryset = queryset.filter(family_id=family)

        active = self.request.query_params.get("active")
        if is_admin_view and active == "true":
            queryset = queryset.filter(is_active=True)
        elif is_admin_view and active == "false":
            queryset = queryset.filter(is_active=False)

        return queryset.order_by("first_name")


class FamilyMemberRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FamilyMemberSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        if self.request.method == "DELETE":
            return [IsAuthenticated(), IsSuperAdmin()]
        return [IsAuthenticated(), CanManageFamilyMembers()]

    def get_queryset(self):
        queryset = FamilyMember.objects.select_related("family", "family__family_unit")

        user = self.request.user
        is_admin_view = (
            self.request.method == "GET"
            and user.is_authenticated
            and has_permission(
                user,
                UserPermission.PermissionChoices.MANAGE_FAMILY_MEMBERS,
            )
        )

        if self.request.method == "GET" and not is_admin_view:
            return queryset.filter(is_active=True)

        return queryset