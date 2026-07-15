from django.contrib.auth.models import AbstractUser
from django.db import models
import secrets
from datetime import timedelta
from django.utils import timezone
import uuid
from .managers import UserManager

class UserRole(models.TextChoices):
    SUPERADMIN = "SUPERADMIN", "Super Admin"
    STAFF = "STAFF", "Staff"
    GROUP_LEADER = "GROUP_LEADER", "Group Leader"
    FAMILY_UNIT_PRESIDENT = "FAMILY_UNIT_PRESIDENT", "Family Unit President"


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        max_length=20,
        blank=True,
    )

    role = models.CharField(
        max_length=30,
        choices=UserRole.choices,
        default=UserRole.STAFF,
    )

    is_email_verified = models.BooleanField(default=False)

    must_change_password = models.BooleanField(default=True)

    invited_by = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="invited_users",
    )

    USERNAME_FIELD = "email"

    # REQUIRED_FIELDS = ["username"]

    REQUIRED_FIELDS = []
    objects = UserManager()

    @property
    def full_name(self):
        return (
            f"{self.first_name} {self.last_name}"
        ).strip()
    
    class Meta:
        ordering = ["email"]


class Invitation(models.Model):

    class Status(models.TextChoices):

        PENDING = "PENDING", "Pending"
        ACCEPTED = "ACCEPTED", "Accepted"
        CANCELLED = "CANCELLED", "Cancelled"
        EXPIRED = "EXPIRED", "Expired"

    email = models.EmailField(unique=True)

    role = models.CharField(
        max_length=30,
        choices=UserRole.choices,
    )

    token = models.CharField(
        max_length=64,
        unique=True,
        editable=False,
    )

    invited_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_invitations",
    )

    expires_at = models.DateTimeField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]

    @staticmethod
    def generate_token():
        return secrets.token_urlsafe(32)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_token()

        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(days=7)

        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"{self.email} ({self.role})"
    
class UserSession(models.Model):

    user = models.ForeignKey(

        User,

        on_delete=models.CASCADE,

        related_name="sessions",

    )

    session_id = models.UUIDField(

        default=uuid.uuid4,

        unique=True,

        editable=False,

    )

    token_version = models.PositiveIntegerField(

        default=1,

    )

    ip_address = models.GenericIPAddressField(

        null=True,

        blank=True,

    )

    user_agent = models.TextField(

        blank=True,

    )

    is_active = models.BooleanField(

        default=True,

    )

    last_activity = models.DateTimeField(

        auto_now=True,

    )

    created_at = models.DateTimeField(

        auto_now_add=True,

    )


    def __str__(self):

        return (

            f"{self.user.email} - "

            f"{self.session_id}"

        )
    
    class Meta:

        ordering = ["-created_at"]

        indexes = [

            models.Index(

                fields=["user", "is_active"]

            ),

            models.Index(

                fields=["session_id"]

            ),

        ]
    

class LoginHistory(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="login_history",
    )

    session = models.ForeignKey(

        UserSession,

        on_delete=models.SET_NULL,

        null=True,

        blank=True,

        related_name="history",

    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
    )

    user_agent = models.TextField(
        blank=True,
    )

    login_time = models.DateTimeField(
        auto_now_add=True,
    )

    logout_time = models.DateTimeField(
        null=True,
        blank=True,
    )

    is_successful = models.BooleanField(
        default=True,
    )

    class Meta:

        ordering = ["-login_time"]

        indexes = [

            models.Index(

                fields=["user"]

            ),

            models.Index(

                fields=["login_time"]

            ),

    ]

    def __str__(self):
        return (
            f"{self.user.email} - "
            f"{self.login_time}"
        )
    
class PasswordResetToken(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="password_reset_tokens",
    )

    token = models.CharField(
        max_length=64,
        unique=True,
        editable=False,
    )

    expires_at = models.DateTimeField()

    is_used = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]

    @staticmethod
    def generate_token():
        return secrets.token_urlsafe(32)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_token()

        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=1)

        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return self.user.email
    
    