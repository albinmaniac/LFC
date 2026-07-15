from django.db.models import Q
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import (AllowAny,IsAuthenticated,)
from accounts.permissions import (IsSuperAdmin,)
from lfc_project.pagination import StandardPagination
from .models import Staff
from django.db.models import OuterRef, Subquery
from accounts.models import Invitation
from .serializers import (
    StaffCreateUpdateSerializer,
    StaffDetailSerializer,
    StaffListSerializer,)


class StaffListCreateAPIView(generics.ListCreateAPIView):

    pagination_class = StandardPagination

    def get_serializer_class(self):

        if self.request.method == "POST":
            return StaffCreateUpdateSerializer

        return StaffListSerializer

    def get_permissions(self):

        if self.request.method == "POST":
            return [
                IsAuthenticated(),
                IsSuperAdmin(),
            ]

        return [AllowAny()]

    def get_queryset(self):
        latest_invitation = Invitation.objects.filter(
            email__iexact=OuterRef("email")
        ).order_by("-created_at")

        queryset = Staff.objects.annotate(
            invitation_status=Subquery(
                latest_invitation.values("status")[:1]
            )
        ).order_by("name")

        search = self.request.query_params.get("search")
        designation = self.request.query_params.get("designation")
        active = self.request.query_params.get("is_active")

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search)
                | Q(email__icontains=search)
                | Q(phone_number__icontains=search)
                | Q(designation__icontains=search)
            )

        if designation:
            queryset = queryset.filter(designation=designation)

        if active in ["true", "false"]:
            queryset = queryset.filter(is_active=(active == "true"))

        user = self.request.user

        if (
            user.is_authenticated
            and user.is_active
            and IsSuperAdmin().has_permission(
                self.request,
                self,
            )
        ):
            return queryset

        return queryset.filter(
            is_active=True,
        )


class StaffRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Staff.objects.all()
    pagination_class = StandardPagination
    lookup_field = "pk"

    def get_serializer_class(self):

        if self.request.method in [
            "PUT",
            "PATCH",
        ]:
            return StaffCreateUpdateSerializer

        return StaffDetailSerializer

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
                IsSuperAdmin(),
            ]

        return [IsAuthenticated()]

    def get_queryset(self):

        latest_invitation = Invitation.objects.filter(
            email__iexact=OuterRef("email")
        ).order_by("-created_at")

        queryset = Staff.objects.annotate(
            invitation_status=Subquery(
                latest_invitation.values("status")[:1]
            )
        ).order_by("name")

        user = self.request.user

        if (
            user.is_authenticated
            and user.is_active
            and IsSuperAdmin().has_permission(
                self.request,
                self,
            )
        ):
            return queryset

        return queryset.filter(is_active=True)


# Deactivate/Reactivate staff endpoints
class StaffDeactivateAPIView(generics.GenericAPIView):
    queryset = Staff.objects.all()
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def post(self, request, pk):
        staff = self.get_object()
        staff.is_active = False
        staff.save(update_fields=["is_active"])
        return Response({"message": "Staff deactivated successfully."}, status=status.HTTP_200_OK)


class StaffReactivateAPIView(generics.GenericAPIView):
    queryset = Staff.objects.all()
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def post(self, request, pk):
        staff = self.get_object()
        staff.is_active = True
        staff.save(update_fields=["is_active"])
        return Response({"message": "Staff reactivated successfully."}, status=status.HTTP_200_OK)