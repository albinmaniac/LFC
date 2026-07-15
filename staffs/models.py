from django.db import models
from lfc_project.validators import validate_image


class Staff(models.Model):
    name = models.CharField(
        max_length=255,
    )

    email = models.EmailField(
        blank=True,
    )

    phone_number = models.CharField(
        max_length=20,
        blank=True,
    )

    designation = models.CharField(
        max_length=255,
        db_index=True,
    )

    photo = models.ImageField(
        upload_to="staffs/photos/",
        blank=True,
        null=True,
        validators=[validate_image],
    )


    bio = models.TextField(
        blank=True,
    )

    start_date = models.DateField(
        null=True,
        blank=True,
    )

    end_date = models.DateField(
        null=True,
        blank=True,
    )

    show_email_publicly = models.BooleanField(
        default=False,
        verbose_name="Display email on public website",
    )

    show_phone_publicly = models.BooleanField(
        default=False,
        verbose_name="Display phone number on public website",
    )

    class StaffStatus(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        RETIRED = "RETIRED", "Retired"
        TRANSFERRED = "TRANSFERRED", "Transferred"
        RESIGNED = "RESIGNED", "Resigned"

    status = models.CharField(
        max_length=20,
        choices=StaffStatus.choices,
        default=StaffStatus.ACTIVE,
        db_index=True,
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Staff"
        verbose_name_plural = "Staffs"
        indexes = [
            models.Index(fields=["is_active"]),
            models.Index(fields=["designation"]),
            models.Index(fields=["status"]),
            models.Index(fields=["start_date"]),
        ]

    def clean(self):
        if self.designation:
            self.designation = self.designation.strip()

        if (
            self.start_date
            and self.end_date
            and self.end_date < self.start_date
        ):
            from django.core.exceptions import ValidationError

            raise ValidationError(
                {
                    "end_date": (
                        "End date cannot be earlier than start date."
                    )
                }
            )

        if self.end_date and self.status == self.StaffStatus.ACTIVE:
            self.status = self.StaffStatus.TRANSFERRED

    def __str__(self):
        return f"{self.name} - {self.designation}"
