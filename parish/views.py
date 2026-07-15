from django.utils import timezone
from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import (IsAuthenticated,AllowAny,)
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from django.db import transaction
from django.shortcuts import get_object_or_404
from accounts.permissions import (
    IsSuperAdmin,
    CanViewDashboard,
    CanManageSettings,
)
from staffs.models import Staff
from families.models import (
    Family,
    FamilyMember,
    FamilyUnit,
)
from events.models import Event
from notices.models import Notice
from gallery.models import (
    Album,
    Photo,
)
from accounts.models import User
from parish.models import (
    Parish,
    MassTiming,
    UserPermission,
)
from parish.serializers import (
        AssignPermissionSerializer,
        ParishSerializer,
        ParishUpdateSerializer,
        UserPermissionBulkSerializer,
        UserPermissionSerializer,
        MassTimingSerializer,
    )


class ParishDetailAPIView(APIView):
    """
    Public endpoint.
    Returns the parish information.
    """

    permission_classes = [AllowAny]

    def get(self, request):

        parish = (
            Parish.objects
            .prefetch_related("mass_timings")
            .first()
        )

        if not parish:
            return Response(
                {
                    "detail": "Parish information not configured."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = ParishSerializer(parish)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
    
    def get_parish(self):
        parish = Parish.objects.prefetch_related("mass_timings").first()
        if parish is None:
            parish = Parish.objects.create()
        return parish
    

class ParishUpdateAPIView(APIView):
    """
    Allows superadmin to update parish information.
    """
    permission_classes = [
        IsAuthenticated,
        IsSuperAdmin,
    ]

    def put(self, request):

        parish = (
            Parish.objects
            .prefetch_related("mass_timings")
            .first()
        )

        if not parish:
            return Response(
                {
                    "detail": "Parish not configured."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = ParishUpdateSerializer(
            parish,
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True
        )

        with transaction.atomic():
            serializer.save()

        return Response(
            ParishSerializer(parish, context={"request": request}).data,
            status=status.HTTP_200_OK,
        )

    def patch(self, request):

        parish = (
            Parish.objects
            .prefetch_related("mass_timings")
            .first()
        )

        if not parish:
            return Response(
                {
                    "detail": "Parish not configured."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = ParishUpdateSerializer(
            parish,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(
            raise_exception=True
        )

        with transaction.atomic():
            serializer.save()

        return Response(
            ParishSerializer(parish, context={"request": request}).data,
            status=status.HTTP_200_OK,
        )


# MassTiming CRUD Views
class MassTimingListCreateAPIView(ListCreateAPIView):

    serializer_class = MassTimingSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), CanManageSettings()]

    def get_queryset(self):
        queryset = MassTiming.objects.select_related("parish")

        if self.request.method == "GET":
            queryset = queryset.filter(is_active=True)

        return queryset.order_by("day", "mass_time")

    def perform_create(self, serializer):
        parish = Parish.objects.first()

        if parish is None:
            raise serializers.ValidationError(
                {
                    "parish": "Please configure the parish before adding Mass Timings."
                }
            )

        serializer.save(parish=parish)


class MassTimingRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):

    serializer_class = MassTimingSerializer
    queryset = MassTiming.objects.select_related("parish")
    permission_classes = [
        IsAuthenticated,
        CanManageSettings,
    ]

    def perform_destroy(self, instance):
        instance.delete()

class PermissionListCreateAPIView(APIView):
    """
    Superadmin endpoint to list and assign user permissions.
    """
    permission_classes = [
        IsAuthenticated,
        IsSuperAdmin,
    ]

    def get(self, request):

        permissions = UserPermission.objects.select_related(
            "user"
        ).order_by(
            "user__email",
            "permission",
        )

        serializer = UserPermissionSerializer(
            permissions,
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def post(self, request):

        serializer = AssignPermissionSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        permission = serializer.save()

        return Response(
            UserPermissionSerializer(permission).data,
            status=status.HTTP_201_CREATED,
        )


class UserPermissionsAPIView(APIView):
    """
    Superadmin endpoint to retrieve all permissions for a user.
    """
    permission_classes = [
        IsAuthenticated,
        IsSuperAdmin,
    ]

    def get(self, request, user_id):
        user = get_object_or_404(
            User,
            pk=user_id,
        )

        permissions = UserPermission.objects.filter(
            user=user,
        ).order_by(
            "permission"
        )

        serializer = UserPermissionSerializer(
            permissions,
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class UserPermissionDeleteAPIView(APIView):
    """
    Superadmin endpoint to delete a user's permission.
    """
    permission_classes = [
        IsAuthenticated,
        IsSuperAdmin,
    ]

    def delete(self, request, pk):
        permission = get_object_or_404(
            UserPermission,
            pk=pk,
        )
        permission.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )


class UserPermissionBulkUpdateAPIView(APIView):
    """
    Superadmin endpoint for bulk updating a user's permissions.
    """
    permission_classes = [
        IsAuthenticated,
        IsSuperAdmin,
    ]

    def put(self, request):

        serializer = UserPermissionBulkSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        user_id = serializer.validated_data[
            "user_id"
        ]

        permissions = serializer.validated_data[
            "permissions"
        ]

        user = get_object_or_404(
            User,
            pk=user_id,
        )

        permissions = list(
            dict.fromkeys(permissions)
        )

        with transaction.atomic():

            UserPermission.objects.filter(
                user=user,
            ).delete()

            records = [
                UserPermission(
                    user=user,
                    permission=permission,
                )
                for permission in permissions
            ]

            if records:
                UserPermission.objects.bulk_create(
                    records,
                )

        updated_permissions = (
            UserPermission.objects
            .select_related("user")
            .filter(user=user)
            .order_by("permission")
        )

        return Response(
            {
                "message": "Permissions updated successfully.",
                "permissions": UserPermissionSerializer(
                    updated_permissions,
                    many=True,
                ).data,
            },
            status=status.HTTP_200_OK,
        )
    

class DashboardAPIView(APIView):
    """
    Returns dashboard statistics. Requires CanViewDashboard permission.
    """
    permission_classes = [
        IsAuthenticated,
        CanViewDashboard,
    ]

    def get(self, request):

        parish = Parish.objects.first()

        data = {

            "parish": {
                "name": parish.name if parish else None,
                "diocese": parish.diocese if parish else None,
                "patron_saint": parish.patron_saint if parish else None,
                "mass_timings": MassTiming.objects.filter(
                    is_active=True,
                ).count(),
            },

            "staffs": {
                "total": Staff.objects.count(),
                "active": Staff.objects.filter(
                    is_active=True,
                ).count(),
            },

            "family_units": {
                "total": FamilyUnit.objects.count(),
                "active": FamilyUnit.objects.filter(
                    is_active=True,
                ).count(),
            },

            "families": {
                "total": Family.objects.count(),
                "active": Family.objects.filter(
                    is_active=True,
                ).count(),
            },

            "family_members": {
                "total": FamilyMember.objects.count(),
            },

            "events": {
                "upcoming": Event.objects.filter(
                    is_active=True,
                    start_datetime__gte=timezone.now(),
                ).count(),

                "featured": Event.objects.filter(
                    is_active=True,
                    is_featured=True,
                ).count(),
            },

            "notices": {
                "active": Notice.objects.filter(
                    is_active=True,
                ).count(),

                "featured": Notice.objects.filter(
                    is_active=True,
                    is_featured=True,
                ).count(),
            },

            "gallery": {
                "albums": Album.objects.filter(
                    is_active=True,
                ).count(),

                "photos": Photo.objects.filter(
                    is_active=True,
                ).count(),
            },
        }

        return Response(
            data,
            status=status.HTTP_200_OK,
        )
    
