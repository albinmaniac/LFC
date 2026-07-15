
from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from lfc_project.pagination import GalleryPagination
from accounts.permissions import (CanManageGallery,IsSuperAdmin,)
from .models import Album, Photo
from .serializers import (AlbumSerializer,PhotoSerializer,)


class AlbumListCreateAPIView(
        generics.ListCreateAPIView
    ):

    serializer_class = AlbumSerializer
    pagination_class = GalleryPagination

    filter_backends = [
        SearchFilter,
        OrderingFilter,
    ]

    search_fields = [
        "title",
        "description",
        "event__title",
    ]

    ordering_fields = [
        "title",
        "created_at",
    ]

    ordering = [
        "-created_at",
    ]

    def get_permissions(self):

        if self.request.method == "GET":
            return [AllowAny()]

        return [
            IsAuthenticated(),
            CanManageGallery(),
        ]

    def get_queryset(self):

        queryset = (
            Album.objects
            .select_related("event")
            .prefetch_related("photos")
        )

        if self.request.method == "GET":
            queryset = queryset.filter(
                is_active=True,
                is_public=True,
            )

        event_id = self.request.query_params.get(
            "event"
        )

        featured = self.request.query_params.get(
            "featured"
        )

        active = self.request.query_params.get(
            "active"
        )

        if event_id:
            queryset = queryset.filter(
                event_id=event_id,
            )

        if featured == "true":
            queryset = queryset.filter(
                is_featured=True,
            )

        if active == "true":
            queryset = queryset.filter(
                is_active=True,
            )

        return queryset


class AlbumRetrieveUpdateDestroyAPIView(
        generics.RetrieveUpdateDestroyAPIView
    ):

    serializer_class = AlbumSerializer

    def get_permissions(self):

        if self.request.method == "GET":
            return [AllowAny()]

        if self.request.method == "DELETE":
            return [
                IsAuthenticated(),
                IsSuperAdmin(),
            ]

        return [
            IsAuthenticated(),
            CanManageGallery(),
        ]

    def get_queryset(self):

        queryset = (
            Album.objects
            .select_related("event")
            .prefetch_related("photos")
        )

        if self.request.method == "GET":
            return queryset.filter(
                is_active=True,
                is_public=True,
            )

        return queryset


class PhotoListCreateAPIView(
        generics.ListCreateAPIView
    ):

    serializer_class = PhotoSerializer
    pagination_class = GalleryPagination

    filter_backends = [
        SearchFilter,
        OrderingFilter,
    ]

    search_fields = [
        "caption",
        "album__title",
    ]

    ordering_fields = [
        "display_order",
        "created_at",
    ]

    ordering = [
        "display_order",
        "id",
    ]

    def get_permissions(self):

        if self.request.method == "GET":
            return [AllowAny()]

        return [
            IsAuthenticated(),
            CanManageGallery(),
        ]

    def get_queryset(self):

        queryset = (
            Photo.objects
            .select_related("album")
        )

        if self.request.method == "GET":
            queryset = queryset.filter(
                is_active=True,
                album__is_active=True,
                album__is_public=True,
            )

        album_id = self.request.query_params.get(
            "album"
        )

        if album_id:
            queryset = queryset.filter(
                album_id=album_id,
            )

        return queryset


class PhotoRetrieveUpdateDestroyAPIView(
        generics.RetrieveUpdateDestroyAPIView
    ):

    serializer_class = PhotoSerializer

    def get_permissions(self):

        if self.request.method == "GET":
            return [AllowAny()]

        if self.request.method == "DELETE":
            return [
                IsAuthenticated(),
                IsSuperAdmin(),
            ]

        return [
            IsAuthenticated(),
            CanManageGallery(),
        ]

    def get_queryset(self):

        queryset = Photo.objects.select_related(
            "album"
        )

        if self.request.method == "GET":
            return queryset.filter(
                is_active=True,
                album__is_active=True,
                album__is_public=True,
            )

        return queryset


class FeaturedAlbumListAPIView(
        generics.ListAPIView
    ):

    serializer_class = AlbumSerializer
    permission_classes = [AllowAny]
    pagination_class = GalleryPagination

    def get_queryset(self):

        return (
            Album.objects
            .select_related("event")
            .prefetch_related("photos")
            .filter(
                is_active=True,
                is_public=True,
                is_featured=True,
            )
            .order_by("-created_at")
        )
