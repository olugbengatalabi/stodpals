from django.urls import path
from . import views
urlpatterns = [
    path("", views.getRoutes, name = "api"),
    path("get-rooms", views.getRooms, name = "roomsapi"),
    path("get-room/<str:pk>", views.getRoom, name = "roomapi"),
]
