from django.urls import path, include
from rest_framework import routers
from .resources import EmployeesModelViewSet, OrganizationsModelViewSet, DepartmentsModelViewSet

router = routers.SimpleRouter()
router.register('employees', EmployeesModelViewSet)
router.register('departments', DepartmentsModelViewSet)
router.register('organizations', OrganizationsModelViewSet)

urlpatterns = [
    path('taskapp/', include(router.urls)),

]
