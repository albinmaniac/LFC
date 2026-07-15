

from rest_framework import serializers

from .models import Album, Photo


class PhotoSerializer(serializers.ModelSerializer):

    image_url = serializers.SerializerMethodField()
    album_title = serializers.CharField(
        source="album.title",
        read_only=True,
    )

    class Meta:
        model = Photo

        fields = (
            "id",
            "album",
            "album_title",
            "image",
            "image_url",
            "caption",
            "display_order",
            "is_active",
            "created_at",
        )

        read_only_fields = (
            "id",
            "created_at",
        )

    def validate_caption(self, value):

        value = value.strip()

        if value and len(value) < 2:
            raise serializers.ValidationError(
                "Caption must contain at least 2 characters."
            )

        return value

    def get_image_url(self, obj):

        request = self.context.get("request")

        if obj.image:

            if request:
                return request.build_absolute_uri(
                    obj.image.url,
                )

            return obj.image.url

        return None


class AlbumSerializer(serializers.ModelSerializer):

    cover_image_url = serializers.SerializerMethodField()

    photo_count = serializers.SerializerMethodField()

    event_title = serializers.CharField(
        source="event.title",
        read_only=True,
    )

    photos = PhotoSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Album

        fields = (
            "id",
            "title",
            "description",
            "cover_image",
            "cover_image_url",
            "event",
            "event_title",
            "photo_count",
            "photos",
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
            "photo_count",
        )

    def validate_title(self, value):

        value = value.strip()

        if len(value) < 3:
            raise serializers.ValidationError(
                "Album title must contain at least 3 characters."
            )

        return value

    def validate_description(self, value):

        value = value.strip()

        return value

    def validate(self, attrs):

        is_public = attrs.get(
            "is_public",
            getattr(self.instance, "is_public", True),
        )

        is_featured = attrs.get(
            "is_featured",
            getattr(self.instance, "is_featured", False),
        )

        if is_featured and not is_public:
            raise serializers.ValidationError(
                {
                    "is_featured": (
                        "Featured albums must be public."
                    )
                }
            )

        title = attrs.get(
            "title",
            getattr(self.instance, "title", None),
        )

        if title:

            queryset = Album.objects.filter(
                title__iexact=title.strip(),
            )

            if self.instance:
                queryset = queryset.exclude(
                    pk=self.instance.pk,
                )

            if queryset.exists():
                raise serializers.ValidationError(
                    {
                        "title": (
                            "An album with this title already exists."
                        )
                    }
                )

        return attrs

    def get_cover_image_url(self, obj):

        request = self.context.get("request")

        if obj.cover_image:

            if request:
                return request.build_absolute_uri(
                    obj.cover_image.url,
                )

            return obj.cover_image.url

        return None

    def get_photo_count(self, obj):
        return obj.photos.filter(
            is_active=True,
        ).count()
    
    