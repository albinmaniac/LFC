from django.utils import timezone
from rest_framework import status, generics
from rest_framework.permissions import (IsAuthenticated,AllowAny,)
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from django.db.models import Q
from accounts.permissions import IsSuperAdmin
from accounts.serializers import (
    ForgotPasswordSerializer,
    UserSerializer,
    UserProfileSerializer,
    LoginSerializer,
    LoginUserSerializer,
    InvitationCreateSerializer,
    InvitationListSerializer,
    AcceptInvitationSerializer,
    UserSessionSerializer,
    LoginHistorySerializer,
    ChangePasswordSerializer,
    ResetPasswordSerializer,
    
)
from rest_framework import exceptions
from accounts.email_service import InvitationService, PasswordResetService,SecurityEmailService,AccountEmailService
from lfc_project.pagination import StandardPagination
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import (
    User,
    Invitation,
    UserSession,
    LoginHistory,
    UserRole,
    PasswordResetToken,
)
from rest_framework_simplejwt.views import TokenRefreshView
from parish.models import UserPermission
from accounts.throttles import (
    LoginRateThrottle,
    PasswordResetRateThrottle,
    InvitationRateThrottle,
    RefreshTokenRateThrottle,
)
import logging
logger = logging.getLogger(__name__)
# Returns active users for admin password reset dropdown

class CustomTokenRefreshView(TokenRefreshView):

    throttle_classes = [RefreshTokenRateThrottle]

class PasswordResetUserListAPIView(generics.ListAPIView):
    """Returns active users that can receive an admin password reset."""

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    pagination_class = StandardPagination

    def get_queryset(self):
        queryset = (
            User.objects.filter(is_active=True)
            .only("id", "full_name", "username", "email", "role", "is_active")
            .order_by("full_name", "email")
        )

        search = self.request.query_params.get("search")
        role = self.request.query_params.get("role")

        if search:
            queryset = queryset.filter(
                Q(full_name__icontains=search)
                | Q(email__icontains=search)
                | Q(username__icontains=search)
            )

        if role:
            queryset = queryset.filter(role=role)

        return queryset



class CurrentUserAPIView(APIView):
    """Retrieve or update the current authenticated user."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_data = UserSerializer(request.user).data

        if _is_super_admin(request.user):
            permissions = [
                choice[0]
                for choice in UserPermission.PermissionChoices.choices
            ]
        else:
            permissions = list(
                UserPermission.objects.filter(user=request.user)
                .values_list("permission", flat=True)
            )

        return Response(
            {
                "user": user_data,
                "permissions": permissions,
            },
            status=status.HTTP_200_OK,
        )



class MyProfileAPIView(APIView):
    """
    Retrieve and update the authenticated user's own profile.
    Note: This endpoint is intentionally separate from CurrentUserAPIView so users can edit only self-service profile fields while admin-managed fields remain protected.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(
            request.user,
            context={"request": request},
        )
        return Response(
            {
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    @transaction.atomic
    def patch(self, request):
        serializer = UserProfileSerializer(
            request.user,
            data=request.data,
            partial=True,
            context={"request": request},
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "message": "Profile updated successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

# Change password endpoint
class ChangePasswordAPIView(APIView):
    """Change the password for the current authenticated user."""
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)

        request.user.set_password(
            serializer.validated_data["new_password"]
        )
        request.user.must_change_password = False
        request.user.save(
            update_fields=[
                "password",
                "must_change_password",
            ]
        )

        frontend_url = getattr(
            settings,
            "ADMIN_FRONTEND_URL",
            "http://localhost:5173",
        )

        try:
            SecurityEmailService.send_password_changed_email(
                user=request.user,
                changed_at=timezone.now(),
                changed_ip=request.META.get("REMOTE_ADDR"),
                changed_device=request.META.get("HTTP_USER_AGENT", ""),
                login_url=f"{frontend_url}/login",
            )
        except Exception:
            logger.exception("Failed to send password-changed email to %s", request.user.email)

        UserSession.objects.filter(
            user=request.user,
            is_active=True,
        ).exclude(
            session_id=request.auth.get("session_id")
            if request.auth
            else None
        ).update(is_active=False)

        LoginHistory.objects.filter(
            user=request.user,
            logout_time__isnull=True,
        ).exclude(
            session__session_id=request.auth.get("session_id")
            if request.auth
            else None
        ).update(logout_time=timezone.now())

        return Response(
            {"message": "Password changed successfully."},
            status=status.HTTP_200_OK,
        )
#
# Admin-triggered password reset view



class SendPasswordResetAPIView(APIView):
    """Send a password reset email to a user (admin only)."""
    throttle_classes = [PasswordResetRateThrottle]
    permission_classes = [
        IsAuthenticated,
        IsSuperAdmin,
    ]

    @transaction.atomic
    def post(self, request, user_id):
        try:
            user = User.objects.get(
                pk=user_id,
                is_active=True,
            )
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        PasswordResetToken.objects.filter(
            user=user,
            is_used=False,
        ).update(is_used=True)

        reset = PasswordResetToken.objects.create(
            user=user,
        )

        frontend_url = getattr(
            settings,
            "ADMIN_FRONTEND_URL",
            "http://localhost:5173",
        )
        reset_link = f"{frontend_url}/reset-password/{reset.token}"

        # Left as a hard failure (unlike the other views) on purpose: a
        # PasswordResetToken that exists but was never emailed is a dead,
        # unusable token, and transaction.atomic + set_rollback keeps the DB
        # clean in that case. This one SHOULD roll back if the email fails.
        try:
            PasswordResetService.send_reset_email(
                user=user,
                reset_link=reset_link,
                requested_ip=request.META.get("REMOTE_ADDR", "Unknown"),
            )

            return Response(
                {
                    "message": "Password reset email sent successfully.",
                    "email": user.email,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as exc:
            logger.exception("Failed to send password reset email to %s", user.email)
            transaction.set_rollback(True)
            return Response(
                {
                    "message": "Failed to send password reset email.",
                    "detail": str(exc),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# ResetPasswordAPIView unchanged
class ResetPasswordAPIView(APIView):
    """Reset a user's password using a reset token."""
    throttle_classes = [PasswordResetRateThrottle]
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request):
        serializer = ResetPasswordSerializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)

        reset_token = serializer.validated_data["reset_token"]
        user = reset_token.user

        user.set_password(
            serializer.validated_data["new_password"]
        )
        user.must_change_password = False
        user.save(
            update_fields=[
                "password",
                "must_change_password",
            ]
        )

        reset_token.is_used = True
        reset_token.save(update_fields=["is_used"])

        UserSession.objects.filter(
            user=user,
            is_active=True,
        ).update(is_active=False)

        LoginHistory.objects.filter(
            user=user,
            logout_time__isnull=True,
        ).update(logout_time=timezone.now())

        return Response(
            {
                "message": "Password reset successfully. Please login with your new password."
            },
            status=status.HTTP_200_OK,
        )

class ForgotPasswordAPIView(APIView):
    """
    Public forgot-password endpoint.

    Always returns the same response to prevent
    email enumeration attacks.
    """

    permission_classes = [AllowAny]
    throttle_classes = [PasswordResetRateThrottle]

    @transaction.atomic
    def post(self, request):
        serializer = ForgotPasswordSerializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        user = (
            User.objects.filter(
                email__iexact=email,
                is_active=True,
            )
            .only("id", "email", "full_name")
            .first()
        )

        # Always return the same response if the account
        # doesn't exist or is inactive.
        if user is None:
            return Response(
                {
                    "message": (
                        "If an account exists with this email, "
                        "a password reset link has been sent."
                    )
                },
                status=status.HTTP_200_OK,
            )

        PasswordResetToken.objects.filter(
            user=user,
            is_used=False,
        ).update(is_used=True)

        reset = PasswordResetToken.objects.create(
            user=user,
        )

        frontend_url = getattr(
            settings,
            "ADMIN_FRONTEND_URL",
            "http://localhost:5173",
        )

        reset_link = (
            f"{frontend_url}/reset-password/{reset.token}"
        )

        try:
            PasswordResetService.send_reset_email(
                user=user,
                reset_link=reset_link,
                requested_ip=request.META.get(
                    "REMOTE_ADDR",
                    "Unknown",
                ),
            )
        except Exception:
            logger.exception(
                "Failed to send forgot-password email to %s",
                user.email,
            )
            transaction.set_rollback(True)

        return Response(
            {
                "message": (
                    "If an account exists with this email, "
                    "a password reset link has been sent."
                )
            },
            status=status.HTTP_200_OK,
        )
    

class InvitationCreateAPIView(APIView):
    """Create a new invitation or list invitations (admin only)."""
    throttle_classes = [InvitationRateThrottle]
    permission_classes = [
        IsAuthenticated,
        IsSuperAdmin,
    ]

    def get(self, request):
        Invitation.objects.filter(
            status=Invitation.Status.PENDING,
            expires_at__lt=timezone.now(),
        ).update(status=Invitation.Status.EXPIRED)

        queryset = Invitation.objects.select_related("invited_by").only(
            "id",
            "full_name",
            "email",
            "role",
            "status",
            "expires_at",
            "created_at",
            "invited_by__full_name",
        ).order_by("-created_at")

        search = request.query_params.get("search")
        role = request.query_params.get("role")
        status_filter = request.query_params.get("status")

        if search:
            queryset = queryset.filter(
                Q(email__icontains=search)
                | Q(full_name__icontains=search)
            )

        if role:
            queryset = queryset.filter(role=role)

        if status_filter:
            queryset = queryset.filter(status=status_filter)

        paginator = StandardPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = InvitationListSerializer(
            page,
            many=True,
            context={"request": request},
        )
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = InvitationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # create_invitation() creates the Invitation row THEN sends the
        # email internally (see InvitationService in email_service.py). If
        # the email call raises, the invitation already exists in the DB —
        # which is fine, that's what "Resend Invitation" is for. We just
        # don't want a slow/broken Brevo call to turn a successful
        # invitation into a 500 for the admin.
        try:
            invitation = InvitationService.create_invitation(
                email=serializer.validated_data["email"],
                role=serializer.validated_data["role"],
                permission_snapshot=serializer.validated_data["permission_snapshot"],
                invited_by=request.user,
                full_name=serializer.validated_data["full_name"],
            )
        except Exception:
            logger.exception(
                "Invitation created but email failed to send for %s",
                serializer.validated_data["email"],
            )
            invitation = Invitation.objects.filter(
                email__iexact=serializer.validated_data["email"],
                status=Invitation.Status.PENDING,
            ).order_by("-created_at").first()
            if invitation is None:
                return Response(
                    {"message": "Failed to create invitation.", "detail": "Email delivery failed and no invitation record could be found."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        return Response(
            {
                "message": "Invitation sent successfully.",
                "email": invitation.email,
                "role": invitation.role,
                "expires_at": invitation.expires_at,
            },
            status=status.HTTP_201_CREATED,
        )
    
# Accept invitation API view
class AcceptInvitationAPIView(APIView):
    """Accept an invitation and activate a user account."""
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request):
        serializer = AcceptInvitationSerializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data["token"]

        try:
            invitation = Invitation.objects.get(
                token=token,
                status=Invitation.Status.PENDING,
            )
        except Invitation.DoesNotExist:
            return Response(
                {
                    "detail": "Invalid invitation token."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if invitation.is_expired:
            invitation.status = Invitation.Status.EXPIRED
            invitation.save(update_fields=["status"])

            return Response(
                {
                    "detail": "Invitation has expired."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user, created = User.objects.get_or_create(
            email=invitation.email,
            defaults={
                "username": invitation.email,
                "role": invitation.role,
                "is_active": True,
                "must_change_password": False,
                "invited_by": invitation.invited_by,
                "full_name": invitation.full_name,
            },
        )

        if not created:
            user.role = invitation.role
            user.full_name = invitation.full_name
            user.is_active = True
            user.must_change_password = False
            user.invited_by = invitation.invited_by

        user.set_password(
            serializer.validated_data["password"]
        )
        user.save(update_fields=[
            "username",
            "role",
            "full_name",
            "is_active",
            "must_change_password",
            "invited_by",
            "password",
        ])

        # Replace any existing permissions with the invitation snapshot
        UserPermission.objects.filter(
            user=user,
        ).delete()

        if invitation.permission_snapshot:
            UserPermission.objects.bulk_create(
                [
                    UserPermission(
                        user=user,
                        permission=permission,
                    )
                    for permission in invitation.permission_snapshot
                ]
            )

        invitation.status = Invitation.Status.ACCEPTED
        invitation.save(update_fields=["status"])

        frontend_url = getattr(
            settings,
            "ADMIN_FRONTEND_URL",
            "http://localhost:5173",
        )

        # Critical: the account is ALREADY active and the password is
        # ALREADY set by this point. A failed welcome email must never
        # block the user from being told their account worked and from
        # being able to log in.
        try:
            AccountEmailService.send_welcome_email(
                user=user,
                login_url=f"{frontend_url}/login",
            )
        except Exception:
            logger.exception("Failed to send welcome email to %s", user.email)

        return Response(
            {
                "message": "Account activated successfully."
            },
            status=status.HTTP_200_OK,
        )
    
class CancelInvitationAPIView(APIView):
    """Cancel a pending invitation (admin only)."""
    permission_classes = [
        IsAuthenticated,
        IsSuperAdmin,
    ]

    @transaction.atomic
    def post(self, request, pk):
        try:
            invitation = Invitation.objects.get(pk=pk)
        except Invitation.DoesNotExist:
            return Response(
                {"detail": "Invitation not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if (
            invitation.status
            != Invitation.Status.PENDING
        ):
            return Response(
                {
                    "detail": (
                        "Only pending invitations can be cancelled."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if invitation.is_expired:
            invitation.status = Invitation.Status.EXPIRED
            invitation.save(update_fields=["status"])

            return Response(
                {
                    "detail": (
                        "Invitation has already expired."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        invitation.status = Invitation.Status.CANCELLED
        invitation.save(update_fields=["status"])

        try:
            InvitationService.send_invitation_cancelled_email(
                invitation=invitation,
                cancelled_by=request.user,
            )
        except Exception:
            logger.exception("Failed to send cancellation email for invitation %s", invitation.email)

        return Response(
            {
                "message": (
                    "Invitation cancelled successfully."
                )
            },
            status=status.HTTP_200_OK,
        )
    
class ResendInvitationAPIView(APIView):
    """Resend an invitation email (admin only)."""
    throttle_classes = [InvitationRateThrottle]
    permission_classes = [
        IsAuthenticated,
        IsSuperAdmin,
    ]

    @transaction.atomic
    def post(self, request, pk):
        try:
            invitation = Invitation.objects.get(pk=pk)
        except Invitation.DoesNotExist:
            return Response(
                {"detail": "Invitation not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if (
            invitation.status
            == Invitation.Status.ACCEPTED
        ):
            return Response(
                {
                    "detail": (
                        "Accepted invitations cannot be resent."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Unlike Create/Cancel, "Resend" whose entire PURPOSE is sending an
        # email should surface a real failure to the admin rather than
        # silently succeeding — a resend that didn't send anything is
        # actively misleading. Keep this one as a hard failure.
        try:
            InvitationService.resend_invitation(invitation)
        except Exception as exc:
            logger.exception("Failed to resend invitation to %s", invitation.email)
            return Response(
                {
                    "message": "Failed to resend invitation.",
                    "detail": str(exc),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {
                "message": (
                    "Invitation resent successfully."
                )
            },
            status=status.HTTP_200_OK,
        )
    
class InvitationDestroyAPIView(generics.DestroyAPIView):
    """Delete an invitation if it is not pending or accepted (admin only)."""
    queryset = Invitation.objects.all()

    permission_classes = [
        IsAuthenticated,
        IsSuperAdmin,
    ]

    def destroy(self, request, *args, **kwargs):
        invitation = self.get_object()

        if invitation.status in [
            Invitation.Status.PENDING,
            Invitation.Status.ACCEPTED,
        ]:
            return Response(
                {
                    "detail": (
                        "This invitation cannot be deleted."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        invitation.delete()

        return Response(
            {
                "message": (
                    "Invitation deleted successfully."
                )
            },
            status=status.HTTP_200_OK,
        )


class LoginAPIView(APIView):
    """Authenticate a user and create a session."""
    throttle_classes = [LoginRateThrottle]
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            self._log_failed_attempt(request)
            raise exceptions.ValidationError(serializer.errors)

        user = serializer.validated_data["user"]
        ip_address = request.META.get("REMOTE_ADDR")
        user_agent = request.META.get("HTTP_USER_AGENT", "")

        session = UserSession.objects.create(
            user=user,
            ip_address=ip_address,
            user_agent=user_agent,
        )

        LoginHistory.objects.create(
            user=user,
            session=session,
            ip_address=ip_address,
            user_agent=user_agent,
            is_successful=True,
        )

        refresh = RefreshToken.for_user(user)
        refresh["session_id"] = str(session.session_id)
        refresh["token_version"] = session.token_version

        access_token = refresh.access_token
        access_token["session_id"] = str(session.session_id)
        access_token["token_version"] = session.token_version

        user_data = LoginUserSerializer(user).data

        if _is_super_admin(user):
            permissions = [choice[0] for choice in UserPermission.PermissionChoices.choices]
        else:
            permissions = list(
                UserPermission.objects.filter(user=user).values_list("permission", flat=True)
            )

        return Response(
            {
                "refresh": str(refresh),
                "access": str(access_token),
                "user": user_data,
                "permissions": permissions,
            },
            status=status.HTTP_200_OK,
        )

    def _log_failed_attempt(self, request):
        email = request.data.get("email")
        if not email:
            return

        user = User.objects.filter(email__iexact=email).first()
        if not user:
            # No matching account — nothing to attach the row to. Logging
            # unknown-email attempts would need a nullable `user` FK on
            # LoginHistory, which isn't the current schema.
            return

        LoginHistory.objects.create(
            user=user,
            session=None,
            ip_address=request.META.get("REMOTE_ADDR"),
            user_agent=request.META.get("HTTP_USER_AGENT", ""),
            is_successful=False,
        )


# New views for session and login management

def _is_super_admin(user):
    return (
        getattr(user, "is_superuser", False)
        or getattr(user, "role", None) == UserRole.SUPERADMIN
        or str(getattr(user, "role", "")).lower() == "superadmin"
    )

class ActiveSessionListAPIView(generics.ListAPIView):
    """List active sessions for the current user, or all if super admin."""
    serializer_class = UserSessionSerializer
    pagination_class = StandardPagination
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        base_qs = UserSession.objects.select_related("user")
        if _is_super_admin(self.request.user):
            return base_qs.filter(
                is_active=True,
            ).order_by(
                "-created_at"
            )

        return base_qs.filter(
            user=self.request.user,
            is_active=True,
        ).order_by(
            "-created_at"
        )


class LoginHistoryListAPIView(generics.ListAPIView):
    """List login history for the current user, or all if super admin."""
    serializer_class = LoginHistorySerializer
    pagination_class = StandardPagination
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        base_qs = LoginHistory.objects.select_related(
            "user",
            "session",
        )
        if _is_super_admin(self.request.user):
            return base_qs.all().order_by(
                "-login_time"
            )

        return base_qs.filter(
            user=self.request.user,
        ).order_by(
            "-login_time"
        )


class LogoutAPIView(APIView):
    """Log out from the current session."""
    permission_classes = [
        IsAuthenticated,
    ]

    @transaction.atomic
    def post(self, request):

        session_id = request.auth.get(
            "session_id"
        )

        if not session_id:
            return Response(
                {
                    "message": "Session not found."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:

            session = UserSession.objects.select_related(
                "user"
            ).get(
                session_id=session_id,
                user=request.user,
                is_active=True,
            )

        except UserSession.DoesNotExist:

            return Response(
                {
                    "message": "Session not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        session.is_active = False
        session.save(
            update_fields=["is_active"]
        )

        LoginHistory.objects.filter(
            session=session,
            logout_time__isnull=True,
        ).update(
            logout_time=timezone.now()
        )

        return Response(
            {
                "message": "Logged out successfully."
            },
            status=status.HTTP_200_OK,
        )


class LogoutAllDevicesAPIView(APIView):
    """Log out from all active sessions for the current user."""
    permission_classes = [
        IsAuthenticated,
    ]

    @transaction.atomic
    def post(self, request):

        UserSession.objects.filter(
            user=request.user,
            is_active=True,
        ).update(
            is_active=False,
        )

        LoginHistory.objects.filter(
            user=request.user,
            logout_time__isnull=True,
        ).update(
            logout_time=timezone.now()
        )

        return Response(
            {
                "message": (
                    "Logged out from all devices successfully."
                )
            },
            status=status.HTTP_200_OK,
        )


class ForceLogoutAPIView(APIView):
    """Terminate a specific user session (admin only)."""
    permission_classes = [
        IsAuthenticated,
        IsSuperAdmin,
    ]

    @transaction.atomic
    def post(self, request, pk):
        try:
            session = UserSession.objects.select_related(
                "user"
            ).get(
                pk=pk,
                is_active=True,
            )
        except UserSession.DoesNotExist:
            return Response(
                {
                    "message": "Session not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        # Prevent super admin from terminating their own session via this endpoint
        current_session_id = request.auth.get("session_id") if hasattr(request, "auth") and request.auth else None
        if current_session_id and str(session.session_id) == str(current_session_id):
            return Response(
                {"message": "Use 'Logout Current Device' to end your own session."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        session.is_active = False
        session.save(update_fields=["is_active"])

        LoginHistory.objects.filter(
            session=session,
            logout_time__isnull=True,
        ).update(logout_time=timezone.now())

        frontend_url = getattr(settings, "ADMIN_FRONTEND_URL", "http://localhost:5173")

        try:
            SecurityEmailService.send_force_logout_email(
                user=session.user,
                logged_out_at=timezone.now(),
                triggered_by=request.user.full_name or request.user.username,
                reason="Your session was terminated by the administrator.",
                login_url=f"{frontend_url}/login",
            )
        except Exception:
            logger.exception("Failed to send force-logout email to %s", session.user.email)

        return Response({"message": "Session terminated successfully."}, status=status.HTTP_200_OK)

        