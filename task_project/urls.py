from django.contrib import admin
from django.urls import path, include
from chat.views import ChatRoomCreateView
from users.views import Login, Registration

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.employees.urls')),
    path('api/', include('api.users.urls')),
    path('chat/', include('chat.urls')),
    path('chat-create/', ChatRoomCreateView.as_view(), name='chat-create'),
    path('login/', Login.as_view(), name='login'),
    path('register/', Registration.as_view(), name='register')

]
