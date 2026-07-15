

from django.urls import path

from .views import (
    ParishGroupListCreateAPIView,
    ParishGroupRetrieveUpdateDestroyAPIView,
    ParishGroupMemberListCreateAPIView,
    ParishGroupMemberRetrieveUpdateDestroyAPIView,
)


urlpatterns = [

    path(
        "groups/",
        ParishGroupListCreateAPIView.as_view(),
        name="parish-group-list-create",
    ),

    path(
        "groups/<int:pk>/",
        ParishGroupRetrieveUpdateDestroyAPIView.as_view(),
        name="parish-group-detail",
    ),

    path(
        "group-members/",
        ParishGroupMemberListCreateAPIView.as_view(),
        name="parish-group-member-list-create",
    ),

    path(
        "group-members/<int:pk>/",
        ParishGroupMemberRetrieveUpdateDestroyAPIView.as_view(),
        name="parish-group-member-detail",
    ),
]