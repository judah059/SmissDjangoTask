from dataclasses import field
from django.contrib import admin
from .models import Employees, Departments, Organizations, EmployeesRequest


admin.site.register(Employees)
admin.site.register(Departments)
admin.site.register(Organizations)
admin.site.register(EmployeesRequest)
# Register your models here.
