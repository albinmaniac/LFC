from django.urls import path

from .views import (
    EventListCreateAPIView,
    EventRetrieveUpdateDestroyAPIView,
    FeaturedEventListAPIView,
    UpcomingEventListAPIView,
)

app_name = "events"

urlpatterns = [

    path("",EventListCreateAPIView.as_view(),name="event-list-create",),

    path("featured/",FeaturedEventListAPIView.as_view(),name="featured-events",),

    path("upcoming/",UpcomingEventListAPIView.as_view(),name="upcoming-events",),

    path("<int:pk>/",EventRetrieveUpdateDestroyAPIView.as_view(),name="event-detail",),
]