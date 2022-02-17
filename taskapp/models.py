from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)


class Organizations(models.Model):
    name = models.CharField(max_length=100)


class Departments(models.Model):
    name = models.CharField(max_length=120)
    organization = models.ForeignKey(Organizations, on_delete=models.CASCADE, default=None)


class Employees(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=120)
    department = models.ForeignKey(Departments, on_delete=models.CASCADE)


# Create your models here.
