from django.urls import path, include
from .resources import CustomAuthToken, ApiRegistration

urlpatterns = [
    path('token-auth/', CustomAuthToken.as_view()),
    path('api-registration/', ApiRegistration.as_view()),

]
