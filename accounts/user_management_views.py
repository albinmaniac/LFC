from django.utils import timezone
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404
from accounts.permissions import IsSuperAdmin
from accounts.serializers import UserSerializer
from lfc_project.pagination import StandardPagination
from accounts.models import User, UserSession, LoginHistory, UserRole



class UserDetailAPIView(generics.RetrieveAPIView):
    """Retrieve details of a specific user (SuperAdmin only)."""

    serializer_class = UserSerializer
    permission_classes = [
        IsAuthenticated,
        IsSuperAdmin,
    ]

    queryset = User.objects.select_related("invited_by").only(
        "id",
        "full_name",
        "username",
        "email",
        "role",
        "is_active",
        "last_login",
        "date_joined",
        "must_change_password",
        "is_email_verified",
        "invited_by",
    )


class UserListAPIView(generics.ListAPIView):
    """List users for User Management (SuperAdmin only)."""

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    pagination_class = StandardPagination

    def get_queryset(self):
        queryset = (
            User.objects
            .select_related("invited_by")
            .only(
                "id",
                "full_name",
                "username",
                "email",
                "role",
                "is_active",
                "last_login",
                "date_joined",
                "must_change_password",
                "is_email_verified",
                "invited_by",
            )
            .order_by("full_name")
        )

        search = self.request.query_params.get("search")
        role = self.request.query_params.get("role")
        status_filter = self.request.query_params.get("status")

        if search:
            queryset = queryset.filter(
                Q(full_name__icontains=search)
                | Q(email__icontains=search)
                | Q(username__icontains=search)
            )

        if role:
            queryset = queryset.filter(role=role)

        if status_filter:
            status_value = status_filter.strip().lower()
            if status_value == "active":
                queryset = queryset.filter(is_active=True)
            elif status_value == "inactive":
                queryset = queryset.filter(is_active=False)

        return queryset


class ActivateUserAPIView(APIView):
    """Activate a user account."""

    permission_classes = [
        IsAuthenticated,
        IsSuperAdmin,
    ]


    @transaction.atomic
    def patch(self, request, pk):
        user = get_object_or_404(User, pk=pk)

        if user == request.user:
            return Response(
                {"detail": "You cannot activate your own account through this endpoint."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user.is_active:
            return Response(
                {"detail": "User is already active."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.is_active = True
        if hasattr(user, "must_change_password"):
            user.must_change_password = False
            user.save(update_fields=["is_active", "must_change_password"])
        else:
            user.save(update_fields=["is_active"])

        return Response(
            {"message": "User activated successfully."},
            status=status.HTTP_200_OK,
        )

class DeactivateUserAPIView(APIView):
    """Deactivate a user account."""

    permission_classes = [
        IsAuthenticated,
        IsSuperAdmin,
    ]


    @transaction.atomic
    def patch(self, request, pk):
        user = get_object_or_404(User, pk=pk)

        if user == request.user:
            return Response(
                {
                    "detail": (
                        "You cannot deactivate your own account."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user.role == UserRole.SUPERADMIN:
            active_superadmins = User.objects.filter(
                role=UserRole.SUPERADMIN,
                is_active=True,
            ).count()

            if active_superadmins <= 1:
                return Response(
                    {
                        "detail": (
                            "Cannot deactivate the last active SuperAdmin."
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        if not user.is_active:
            return Response(
                {"detail": "User is already inactive."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.is_active = False
        user.save(update_fields=["is_active"])

        UserSession.objects.filter(
            user=user,
            is_active=True,
        ).update(is_active=False)

        LoginHistory.objects.filter(
            user=user,
            logout_time__isnull=True,
        ).update(logout_time=timezone.now())

        return Response(
            {"message": "User deactivated successfully."},
            status=status.HTTP_200_OK,
        )
