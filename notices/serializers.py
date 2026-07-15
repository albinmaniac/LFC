

from django.utils import timezone
from rest_framework import serializers

from .models import Notice


class NoticeSerializer(serializers.ModelSerializer):

    attachment_url = serializers.SerializerMethodField()

    notice_type_display = serializers.CharField(
        source="get_notice_type_display",
        read_only=True,
    )

    class Meta:
        model = Notice

        fields = (
            "id",
            "title",
            "notice_type",
            "notice_type_display",
            "content",
            "attachment",
            "attachment_url",
            "publish_date",
            "expiry_date",
            "is_public",
            "is_featured",
            "is_active",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )

    def validate_title(self, value):

        value = value.strip()

        if len(value) < 3:
            raise serializers.ValidationError(
                "Title must contain at least 3 characters."
            )

        return value

    def validate_content(self, value):

        value = value.strip()

        if len(value) < 10:
            raise serializers.ValidationError(
                "Content must contain at least 10 characters."
            )

        return value

    def validate(self, attrs):

        publish_date = attrs.get(
            "publish_date",
            getattr(self.instance, "publish_date", None),
        )

        expiry_date = attrs.get(
            "expiry_date",
            getattr(self.instance, "expiry_date", None),
        )

        is_public = attrs.get(
            "is_public",
            getattr(self.instance, "is_public", True),
        )

        is_featured = attrs.get(
            "is_featured",
            getattr(self.instance, "is_featured", False),
        )

        if (
            publish_date
            and expiry_date
            and expiry_date <= publish_date
        ):
            raise serializers.ValidationError(
                {
                    "expiry_date": (
                        "Expiry date must be after publish date."
                    )
                }
            )

        if is_featured and not is_public:
            raise serializers.ValidationError(
                {
                    "is_featured": (
                        "Featured notices must be public."
                    )
                }
            )

        title = attrs.get(
            "title",
            getattr(self.instance, "title", None),
        )

        if title and publish_date:

            queryset = Notice.objects.filter(
                title__iexact=title.strip(),
                publish_date=publish_date,
            )

            if self.instance:
                queryset = queryset.exclude(
                    pk=self.instance.pk,
                )

            if queryset.exists():
                raise serializers.ValidationError(
                    {
                        "title": (
                            "A notice with this title and publish date already exists."
                        )
                    }
                )

        if (
            self.instance is None
            and publish_date
            and publish_date < timezone.now()
        ):
            raise serializers.ValidationError(
                {
                    "publish_date": (
                        "Publish date cannot be in the past."
                    )
                }
            )

        return attrs

    def get_attachment_url(self, obj):

        request = self.context.get("request")

        if obj.attachment:

            if request:
                return request.build_absolute_uri(
                    obj.attachment.url
                )

            return obj.attachment.url

        return None
    
    