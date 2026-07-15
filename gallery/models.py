from django.core.exceptions import ValidationError
from django.db import models
from lfc_project.validators import (
    validate_image,
    validate_document,
)


class Album(models.Model):

    title = models.CharField(
        max_length=255,
        db_index=True,
    )

    description = models.TextField(
        blank=True,
    )

    cover_image = models.ImageField(
        upload_to="gallery/albums/",
        null=True,
        blank=True,
        validators=[validate_image],
    )

    event = models.ForeignKey(
        "events.Event",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="albums",
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
            "-created_at",
        ]

    def clean(self):

        if self.is_featured and not self.is_public:
            raise ValidationError(
                "Featured albums must be public."
            )

    def save(self, *args, **kwargs):

        self.full_clean()

        super().save(
            *args,
            **kwargs,
        )

    def __str__(self):
        return self.title


class Photo(models.Model):

    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        related_name="photos",
        
    )

    image = models.ImageField(
        upload_to="gallery/photos/",
        validators=[validate_image],
    )

    caption = models.CharField(
        max_length=255,
        blank=True,
    )

    display_order = models.PositiveIntegerField(
        default=0,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        ordering = [
            "display_order",
            "id",
        ]

    def __str__(self):
        return (
            self.caption
            or f"Photo #{self.pk}"
        )
    
    