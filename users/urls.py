from django.urls import path

from .views import ChatRoomListView, Room

urlpatterns = [
    path('', ChatRoomListView.as_view(), name='main'),
    path('<str:room_name>/', Room.as_view(), name='room'),
]
