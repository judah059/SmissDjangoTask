from django.urls import path

from .views import MainPaige, Room

urlpatterns = [
    path('', MainPaige.as_view(), name='main'),
    path('<str:room_name>/', Room.as_view(), name='room'),
]
