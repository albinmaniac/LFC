from django.urls import path

from .views import (
    StaffDeactivateAPIView,
    StaffListCreateAPIView,
    StaffReactivateAPIView,
    StaffRetrieveUpdateDestroyAPIView,
)

app_name = "staffs"

urlpatterns = [
    path(
        "",
        StaffListCreateAPIView.as_view(),
        name="staff-list-create",
    ),

    path(
        "<int:pk>/",
        StaffRetrieveUpdateDestroyAPIView.as_view(),
        name="staff-detail",
    ),

    path(

        "<int:pk>/deactivate/",

        StaffDeactivateAPIView.as_view(),

        name="staff-deactivate",

    ),

    path(

        "<int:pk>/reactivate/",

        StaffReactivateAPIView.as_view(),

        name="staff-reactivate",

    ),
]