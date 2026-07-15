from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags
from datetime import timedelta
from .models import Invitation


class EmailService:
    """
    Base service used by all HTML emails.
    """

    @staticmethod
    def send_html_email(
        *,
        subject,
        template_name,
        context=None,
        recipient_list,
    ):
        base_context = {
            "church_name": getattr(settings, "CHURCH_NAME", "LFC Church"),
            "system_name": getattr(settings, "SYSTEM_NAME", "Church Management System"),
            "support_email": settings.DEFAULT_FROM_EMAIL,
            "support_phone": getattr(settings, "CHURCH_PHONE", ""),
            "church_address": getattr(settings, "CHURCH_ADDRESS", ""),
            "current_year": timezone.now().year,
            "logo_url": getattr(settings, "EMAIL_LOGO_URL", ""),
        }

        base_context.update(context or {})

        html_content = render_to_string(
            template_name,
            context=base_context,
        )

        text_content = strip_tags(html_content)

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=recipient_list,
        )
        email.attach_alternative(
            html_content,
            "text/html",
        )

        email.send(fail_silently=False)

class InvitationService:

    @staticmethod
    def create_invitation(*, email, role, invited_by):
        Invitation.objects.filter(
            email__iexact=email,
            status=Invitation.Status.PENDING,
        ).update(status=Invitation.Status.CANCELLED)

        invitation = Invitation.objects.create(
            email=email,
            role=role,
            invited_by=invited_by,
        )

        InvitationService.send_invitation_email(invitation)

        return invitation

    @staticmethod
    def resend_invitation(invitation):
        invitation.token = Invitation.generate_token()
        invitation.status = Invitation.Status.PENDING
        invitation.expires_at = timezone.now() + timedelta(days=7)
        invitation.save(
            update_fields=[
                "token",
                "status",
                "expires_at",
            ]
        )

        InvitationService.send_invitation_email(invitation)

        return invitation

    @staticmethod
    def send_invitation_email(invitation):
        frontend_url = getattr(
            settings,
            "ADMIN_FRONTEND_URL",
            "http://localhost:5173",
        )

        invitation_link = (
            f"{frontend_url}/setup-password/{invitation.token}"
        )

        EmailService.send_html_email(
            subject="You're Invited to Join LFC Church",
            template_name="emails/invitation_email.html",
            context={
                "invitee_name": invitation.email,
                "inviter_name": invitation.invited_by.get_full_name(),
                "role_display": invitation.get_role_display(),
                "accept_invitation_url": invitation_link,
                "expires_at": invitation.expires_at.strftime(
                    "%d %B %Y, %I:%M %p"
                ),
                "header_image_url": getattr(settings, "EMAIL_INVITATION_URL", ""),
            },
            recipient_list=[invitation.email],
        )


    @staticmethod
    def send_invitation_cancelled_email(
            invitation,
            cancelled_by,
        ):
        EmailService.send_html_email(
            subject="Invitation Cancelled",
            template_name="emails/invitation_cancelled_email.html",
            context={
                "invitee_name": invitation.email,
                "cancelled_by": cancelled_by.get_full_name(),
                "role_display": invitation.get_role_display(),
                "cancelled_at": timezone.now(),
                "header_image_url": getattr(settings, "EMAIL_INVITATION_CANCELLED_URL", ""),
            },
            recipient_list=[invitation.email],
        )

# Dedicated Password Reset Service
class PasswordResetService:

    @staticmethod
    def send_reset_email(
        *,
        user,
        reset_link,
        requested_ip="Unknown",
    ):
        EmailService.send_html_email(
            subject="Reset Your Password",
            template_name="emails/password_reset_email.html",
            context={
                "user_name": user.get_full_name() or user.first_name or user.username,
                "reset_password_url": reset_link,
                "expires_in_minutes": 30,
                "requested_at": timezone.now().strftime("%d %B %Y, %I:%M %p"),
                "requested_ip": requested_ip,
                "header_image_url": getattr(settings, "EMAIL_PASSWORD_RESET_URL", ""),
            },
            recipient_list=[user.email],
        )

class AccountEmailService:

    @staticmethod
    def send_welcome_email(*, user, login_url):
        EmailService.send_html_email(
            subject="Welcome to LFC Church",
            template_name="emails/welcome_email.html",
            context={
                "user_name": user.get_full_name() or user.first_name or user.username,
                "user_email": user.email,
                "role_display": user.get_role_display() if hasattr(user, "get_role_display") else "",
                "login_url": login_url,
                "header_image_url": getattr(settings, "EMAIL_WELCOME_URL", ""),
            },
            recipient_list=[user.email],
        )


class SecurityEmailService:

    @staticmethod
    def send_password_changed_email(
        *,
        user,
        changed_at,
        changed_ip,
        changed_device,
        login_url,
    ):
        EmailService.send_html_email(
            subject="Your Password Was Changed",
            template_name="emails/password_changed_email.html",
            context={
                "user_name": user.get_full_name() or user.first_name or user.username,
                "user_email": user.email,
                "changed_at": changed_at,
                "changed_ip": changed_ip,
                "changed_device": changed_device,
                "login_url": login_url,
                "header_image_url": getattr(settings, "EMAIL_PASSWORD_CHANGED_URL", ""),
            },
            recipient_list=[user.email],
        )

    @staticmethod
    def send_force_logout_email(
        *,
        user,
        logged_out_at,
        triggered_by,
        reason,
        login_url,
    ):
        EmailService.send_html_email(
            subject="You Have Been Logged Out",
            template_name="emails/force_logout_email.html",
            context={
                "user_name": user.get_full_name() or user.first_name or user.username,
                "user_email": user.email,
                "logged_out_at": logged_out_at,
                "triggered_by": triggered_by,
                "reason": reason,
                "login_url": login_url,
                "header_image_url": getattr(settings, "EMAIL_FORCE_LOGOUT_URL", ""),
            },
            recipient_list=[user.email],
        )
        
                