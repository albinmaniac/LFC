

from django.urls import path

from .views import (
    AlbumListCreateAPIView,
    AlbumRetrieveUpdateDestroyAPIView,
    FeaturedAlbumListAPIView,
    PhotoListCreateAPIView,
    PhotoRetrieveUpdateDestroyAPIView,
)

app_name = "gallery"

urlpatterns = [

    path("albums/",AlbumListCreateAPIView.as_view(),name="album-list-create",),

    path("albums/featured/",FeaturedAlbumListAPIView.as_view(),name="featured-albums",),

    path("albums/<int:pk>/",AlbumRetrieveUpdateDestroyAPIView.as_view(),name="album-detail",),

    path("photos/",PhotoListCreateAPIView.as_view(),name="photo-list-create",),

    path("photos/<int:pk>/",PhotoRetrieveUpdateDestroyAPIView.as_view(),name="photo-detail",),
    
]