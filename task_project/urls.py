from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.employees.urls')),
    path('api/', include('api.users.urls')),
    path('chat/', include('users.urls')),

]
