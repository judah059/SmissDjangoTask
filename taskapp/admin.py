from dataclasses import field
from django.contrib import admin
from .models import CustomUser, Employees, Departments, Organizations


admin.site.register(CustomUser)
admin.site.register(Employees)
admin.site.register(Departments)
admin.site.register(Organizations)
# Register your models here.
