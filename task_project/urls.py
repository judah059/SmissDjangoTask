from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from taskapp.API.resources import EmployeesModelViewSet, OrganizationsModelViewSet, DepartmentsModelViewSet, CustomAuthToken, ApiRegistration

router = routers.SimpleRouter()
router.register('employees', EmployeesModelViewSet)
router.register('departments', DepartmentsModelViewSet)
router.register('organizations', OrganizationsModelViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('token-auth/', CustomAuthToken.as_view()),
    path('api-registration/', ApiRegistration.as_view()),
]
