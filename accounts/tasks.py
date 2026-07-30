from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist

from .models import Invitation, User


CELERY_RETRY_OPTIONS = {
    "autoretry_for": (Exception,),
    "retry_backoff": True,
    "retry_backoff_max": 300,
    "retry_jitter": True,
    "retry_kwargs": {"max_retries": 3},
}


@shared_task(name="accounts.send_invitation_email", **CELERY_RETRY_OPTIONS)
def send_invitation_email_task(invitation_id):
    try:
        invitation = (
            Invitation.objects
            .select_related("invited_by")
            .get(id=invitation_id)
        )

        from .email_service import InvitationService
        InvitationService.send_invitation_email(invitation)

    except ObjectDoesNotExist:
        return


# Production tasks
@shared_task(name="accounts.send_invitation_cancelled_email", **CELERY_RETRY_OPTIONS)
def send_invitation_cancelled_email_task(invitation_id, cancelled_by_user_id):
    try:
        invitation = Invitation.objects.get(id=invitation_id)
        cancelled_by = User.objects.get(id=cancelled_by_user_id)

        from .email_service import InvitationService
        InvitationService.send_invitation_cancelled_email(
            invitation,
            cancelled_by,
        )

    except ObjectDoesNotExist:
        return

@shared_task(name="accounts.send_password_reset_email", **CELERY_RETRY_OPTIONS)
def send_password_reset_email_task(user_id, reset_link, requested_ip="Unknown"):
    try:
        user = User.objects.get(id=user_id)
        from .email_service import PasswordResetService
        PasswordResetService.send_reset_email(
            user=user,
            reset_link=reset_link,
            requested_ip=requested_ip,
        )
    except ObjectDoesNotExist:
        return


@shared_task(name="accounts.send_welcome_email", **CELERY_RETRY_OPTIONS)
def send_welcome_email_task(user_id, login_url):
    try:
        user = User.objects.get(id=user_id)
        from .email_service import AccountEmailService
        AccountEmailService.send_welcome_email(
            user=user,
            login_url=login_url,
        )
    except ObjectDoesNotExist:
        return


@shared_task(name="accounts.send_password_changed_email", **CELERY_RETRY_OPTIONS)
def send_password_changed_email_task(
        user_id,
        changed_at,
        changed_ip,
        changed_device,
        login_url,
    ):
    try:
        user = User.objects.get(id=user_id)
        from .email_service import SecurityEmailService
        SecurityEmailService.send_password_changed_email(
            user=user,
            changed_at=changed_at,
            changed_ip=changed_ip,
            changed_device=changed_device,
            login_url=login_url,
        )
    except ObjectDoesNotExist:
        return


@shared_task(name="accounts.send_force_logout_email", **CELERY_RETRY_OPTIONS)
def send_force_logout_email_task(
        user_id,
        logged_out_at,
        triggered_by,
        reason,
        login_url,
    ):
    try:
        user = User.objects.get(id=user_id)
        from .email_service import SecurityEmailService
        SecurityEmailService.send_force_logout_email(
            user=user,
            logged_out_at=logged_out_at,
            triggered_by=triggered_by,
            reason=reason,
            login_url=login_url,
        )
    except ObjectDoesNotExist:
        return