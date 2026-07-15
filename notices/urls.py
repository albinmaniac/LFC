

from django.urls import path

from .views import (
    ActiveNoticeListAPIView,
    FeaturedNoticeListAPIView,
    NoticeListCreateAPIView,
    NoticeRetrieveUpdateDestroyAPIView,
)

app_name = "notices"

urlpatterns = [

    path("",NoticeListCreateAPIView.as_view(),name="notice-list-create",),

    path("featured/",FeaturedNoticeListAPIView.as_view(),name="featured-notices",),

    path("active/",ActiveNoticeListAPIView.as_view(),name="active-notices",),

    path("<int:pk>/",NoticeRetrieveUpdateDestroyAPIView.as_view(),name="notice-detail",),

    
]