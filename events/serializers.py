from django.utils import timezone
from rest_framework import serializers

from .models import Event,Feast


class EventSerializer(serializers.ModelSerializer):

    cover_image_url = serializers.SerializerMethodField()
    event_type_display = serializers.CharField(
        source="get_event_type_display",
        read_only=True,
    )

    family_unit_name = serializers.CharField(
        source="family_unit.family_unit_name",
        read_only=True,
    )
    event_status = serializers.SerializerMethodField()

    class Meta:
        model = Event

        fields = (
            "id",
            "title",
            "event_type",
            "event_type_display",
            "family_unit",
            "family_unit_name",
            "description",
            "venue",
            "start_datetime",
            "end_datetime",
            "cover_image",
            "cover_image_url",
            "is_public",
            "is_featured",
            "is_active",
            "event_status",
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

    def validate_description(self, value):

        value = value.strip()

        if len(value) < 10:
            raise serializers.ValidationError(
                "Description must contain at least 10 characters."
            )

        return value

    def validate_venue(self, value):

        value = value.strip()

        if len(value) < 2:
            raise serializers.ValidationError(
                "Venue must contain at least 2 characters."
            )

        return value

    def validate(self, attrs):

        start_datetime = attrs.get(
            "start_datetime",
            getattr(self.instance, "start_datetime", None),
        )

        end_datetime = attrs.get(
            "end_datetime",
            getattr(self.instance, "end_datetime", None),
        )

        is_featured = attrs.get(
            "is_featured",
            getattr(self.instance, "is_featured", False),
        )

        is_public = attrs.get(
            "is_public",
            getattr(self.instance, "is_public", True),
        )

        if start_datetime and end_datetime:

            if end_datetime <= start_datetime:
                raise serializers.ValidationError(
                    {
                        "end_datetime": (
                            "End datetime must be after start datetime."
                        )
                    }
                )

        if (
            self.instance is None
            and start_datetime
            and start_datetime < timezone.now()
        ):
            raise serializers.ValidationError(
                {
                    "start_datetime": (
                        "Event start datetime cannot be in the past."
                    )
                }
            )

        if is_featured and not is_public:
            raise serializers.ValidationError(
                {
                    "is_featured": (
                        "Featured events must be public."
                    )
                }
            )

        title = attrs.get(
            "title",
            getattr(self.instance, "title", None),
        )

        if title:

            queryset = Event.objects.filter(
                title__iexact=title.strip(),
                start_datetime=start_datetime,
            )

            if self.instance:
                queryset = queryset.exclude(
                    pk=self.instance.pk,
                )

            if queryset.exists():
                raise serializers.ValidationError(
                    {
                        "title": (
                            "An event with this title and start time already exists."
                        )
                    }
                )

        return attrs

    def get_event_status(self, obj):

        if obj.end_datetime < timezone.now():
            return "COMPLETED"

        if obj.start_datetime <= timezone.now() <= obj.end_datetime:
            return "ONGOING"

        return "UPCOMING"

    def get_cover_image_url(self, obj):

        request = self.context.get("request")

        if obj.cover_image:

            if request:
                return request.build_absolute_uri(
                    obj.cover_image.url
                )

            return obj.cover_image.url

        return None

class FeastSerializer(serializers.ModelSerializer):

    cover_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Feast

        fields = (
            "id",
            "title",
            "description",
            "feast_date",
            "cover_image",
            "cover_image_url",
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

    def get_cover_image_url(self, obj):

        request = self.context.get("request")

        if obj.cover_image:
            if request:
                return request.build_absolute_uri(
                    obj.cover_image.url
                )
            return obj.cover_image.url

        return None

    def validate_title(self, value):

        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Title cannot be empty."
            )

        return value

    def validate_description(self, value):

        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Description cannot be empty."
            )

        return value

    def validate(self, attrs):

        title = attrs.get(
            "title",
            getattr(self.instance, "title", None),
        )

        feast_date = attrs.get(
            "feast_date",
            getattr(self.instance, "feast_date", None),
        )

        queryset = Feast.objects.filter(
            title__iexact=title.strip(),
            feast_date=feast_date,
        )

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError(
                {
                    "title": (
                        "A feast with this title already "
                        "exists on the selected date."
                    )
                }
            )

        return attrs

class CalendarItemSerializer(serializers.Serializer):

    TYPE_CHOICES = (
        ("event", "Event"),
        ("feast", "Feast"),
    )

    type = serializers.ChoiceField(
        choices=TYPE_CHOICES,
        read_only=True,
    )

    id = serializers.IntegerField(
        read_only=True,
    )

    title = serializers.CharField(
        read_only=True,
    )

    date = serializers.DateField(
        read_only=True,
    )

    is_featured = serializers.BooleanField(
        read_only=True,
    )

    url = serializers.CharField(
        read_only=True,
    )
