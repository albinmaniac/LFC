
from django.core.exceptions import ValidationError
from django.db import models
from lfc_project.validators import validate_image,validate_document


class Notice(models.Model):

    class NoticeType(models.TextChoices):

        GENERAL = (
            "GENERAL",
            "General",
        )

        PARISH_NOTICE = (
            "PARISH_NOTICE",
            "Parish Notice",
        )

        MARRIAGE_BANN = (
            "MARRIAGE_NOTICE",
            "Marriage Notice",
        )

        FUNERAL_NOTICE = (
            "FUNERAL_NOTICE",
            "Funeral Notice",
        )

        PRAYER_REQUEST = (
            "PRAYER_REQUEST",
            "Prayer Request",
        )

        CATECHISM_NOTICE = (
            "CATECHISM_NOTICE",
            "Catechism Notice",
        )

        YOUTH_NOTICE = (
            "YOUTH_NOTICE",
            "Youth Notice",
        )

        EVENT_NOTICE = (
            "EVENT_NOTICE",
            "Event Notice",
        )

        OTHER = (
            "OTHER",
            "Other",
        )

    title = models.CharField(
        max_length=255,
        db_index=True,
    )

    notice_type = models.CharField(
        max_length=30,
        choices=NoticeType.choices,
    )

    content = models.TextField()

    attachment = models.FileField(
        upload_to="notices/attachments/",
        null=True,
        blank=True,
        validators=[validate_document],
    )

    publish_date = models.DateTimeField()

    expiry_date = models.DateTimeField(
        null=True,
        blank=True,
    )

    is_public = models.BooleanField(
        default=True,
    )

    is_featured = models.BooleanField(
        default=False,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:

        ordering = [
            "-publish_date",
        ]

        indexes = [
            models.Index(fields=["notice_type"]),
            models.Index(fields=["publish_date"]),
            models.Index(fields=["is_public"]),
            models.Index(fields=["is_featured"]),
            models.Index(fields=["is_active"]),
        ]

    def clean(self):

        if (
            self.expiry_date
            and self.expiry_date <= self.publish_date
        ):
            raise ValidationError(
                {
                    "expiry_date": (
                        "Expiry date must be after publish date."
                    )
                }
            )

        if self.is_featured and not self.is_public:
            raise ValidationError(
                {
                    "is_featured": (
                        "Featured notices must be public."
                    )
                }
            )

    def save(self, *args, **kwargs):

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
