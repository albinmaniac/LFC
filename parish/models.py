from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from lfc_project.validators import validate_image


class Parish(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
    )

    logo = models.ImageField(
        upload_to="parish/logo/",
        blank=True,
        null=True,
        validators=[validate_image],
    )

    cover_image = models.ImageField(
        upload_to="parish/covers/",
        blank=True,
        null=True,
        validators=[validate_image],
    )

    address = models.TextField()

    phone = models.CharField(
        max_length=20,
        blank=True,
    )

    email = models.EmailField(
        blank=True,
    )

    website = models.URLField(
        blank=True,
    )

    diocese = models.CharField(
        max_length=255,
        blank=True,
    )

    patron_saint = models.CharField(
        max_length=255,
        blank=True,
    )

    established_year = models.PositiveIntegerField(
        blank=True,
        null=True,
    )


    office_phone = models.CharField(
        max_length=20,
        blank=True,
    )

    office_email = models.EmailField(
        blank=True,
    )

    office_open_time = models.TimeField(
        blank=True,
        null=True,
    )

    office_close_time = models.TimeField(
        blank=True,
        null=True,
    )

    google_map_url = models.URLField(
        blank=True,
    )

    facebook_url = models.URLField(
        blank=True,
    )

    instagram_url = models.URLField(
        blank=True,
    )

    youtube_url = models.URLField(
        blank=True,
    )

    whatsapp_url = models.URLField(
        blank=True,
    )

    history = models.TextField(
        blank=True,
    )

    mission = models.TextField(
        blank=True,
    )

    vision = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Parish"
        verbose_name_plural = "Parish"

    def clean(self):
        if (
            not self.pk
            and Parish.objects.exists()
        ):
            raise ValidationError(
                "Only one parish record is allowed."
            )
        
    

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class MassTiming(models.Model):

    class DayChoices(models.TextChoices):
        MONDAY = "MONDAY", "Monday"
        TUESDAY = "TUESDAY", "Tuesday"
        WEDNESDAY = "WEDNESDAY", "Wednesday"
        THURSDAY = "THURSDAY", "Thursday"
        FRIDAY = "FRIDAY", "Friday"
        SATURDAY = "SATURDAY", "Saturday"
        SUNDAY = "SUNDAY", "Sunday"

    parish = models.ForeignKey(
        Parish,
        on_delete=models.CASCADE,
        related_name="mass_timings",
    )

    day = models.CharField(
        max_length=20,
        choices=DayChoices.choices,
    )

    language = models.CharField(
        max_length=100,
        default="Malayalam",
    )

    mass_time = models.TimeField()

    description = models.CharField(
        max_length=255,
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["day", "mass_time"]
        verbose_name = "Mass Timing"
        verbose_name_plural = "Mass Timings"

    def __str__(self):
        return f"{self.get_day_display()} - {self.mass_time.strftime('%I:%M %p')} ({self.language})"


class UserPermission(models.Model):

    class PermissionChoices(models.TextChoices):

        VIEW_DASHBOARD = (
            "VIEW_DASHBOARD",
            "View Dashboard",
        )

        MANAGE_PARISH = (
            "MANAGE_PARISH",
            "Manage Parish",
        )

        MANAGE_SETTINGS = (
            "MANAGE_SETTINGS",
            "Manage Settings",
        )


        MANAGE_FAMILY_UNITS = (
            "MANAGE_FAMILY_UNITS",
            "Manage Family Units",
        )

        MANAGE_FAMILIES = (
            "MANAGE_FAMILIES",
            "Manage Families",
        )

        MANAGE_FAMILY_MEMBERS = (
            "MANAGE_FAMILY_MEMBERS",
            "Manage Family Members",
        )

        MANAGE_GROUPS = (
            "MANAGE_GROUPS",
            "Manage Groups",
        )

        MANAGE_EVENTS = (
            "MANAGE_EVENTS",
            "Manage Events",
        )

        MANAGE_NOTICES = (
            "MANAGE_NOTICES",
            "Manage Notices",
        )

        MANAGE_GALLERY = (
            "MANAGE_GALLERY",
            "Manage Gallery",
        )

        MANAGE_SECURITY = (
            "MANAGE_SECURITY",
            "Manage Security",
        )

        MANAGE_PERMISSIONS = (
            "MANAGE_PERMISSIONS",
            "Manage Permissions",
        )

        VIEW_REPORTS = (
            "VIEW_REPORTS",
            "View Reports",
        )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="permissions",
    )

    permission = models.CharField(
        max_length=50,
        choices=PermissionChoices.choices,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        verbose_name = "User Permission"
        verbose_name_plural = "User Permissions"

        ordering = [
            "user",
            "permission",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "user",
                    "permission",
                ],
                name="unique_user_permission",
            )
        ]

    def clean(self):

        if (
            self.user.role
            == "SUPERADMIN"
        ):
            raise ValidationError(
                "SuperAdmin does not require permission records."
            )

    def save(
        self,
        *args,
        **kwargs,
    ):
        self.full_clean()
        super().save(
            *args,
            **kwargs,
        )

    def __str__(self):

        return (
            f"{self.user.email}"
            f" - "
            f"{self.get_permission_display()}"
        )
    
