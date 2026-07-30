from django.urls import path

from events.views import (
    EventListCreateAPIView,
    EventRetrieveUpdateDestroyAPIView,
    FeaturedEventListAPIView,
    UpcomingEventListAPIView,
    FeastListCreateAPIView,
    FeastRetrieveUpdateDestroyAPIView,
    FeaturedFeastListAPIView,
    CalendarAPIView,
)

app_name = "events"

urlpatterns = [

    path("",EventListCreateAPIView.as_view(),name="event-list-create",),

    path("featured/",FeaturedEventListAPIView.as_view(),name="featured-events",),

    path("upcoming/",UpcomingEventListAPIView.as_view(),name="upcoming-events",),

    path("<int:pk>/",EventRetrieveUpdateDestroyAPIView.as_view(),name="event-detail",),

    path("feasts/",FeastListCreateAPIView.as_view(),name="feast-list-create",),

    path("feasts/<int:pk>/",FeastRetrieveUpdateDestroyAPIView.as_view(),name="feast-detail",),

    path("feasts/featured/",FeaturedFeastListAPIView.as_view(),name="featured-feasts",),

    path("calendar/",CalendarAPIView.as_view(),name="calendar",),

    
]