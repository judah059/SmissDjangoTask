from dataclasses import field, fields
import email
from functools import total_ordering
from rest_framework import serializers
from taskapp.models import CustomUser, Employees, Organizations, Departments
from rest_framework.serializers import ModelSerializer
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import get_user_model
from django.db.models import Sum, Count

UserModel = get_user_model()


class CustomUserGetSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', )


class CustomUserPostSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = UserModel.objects.create_user(username=validated_data['username'], email=validated_data['email'], password=validated_data['password'])
        return user

    class Meta:
        model = UserModel
        fields = ('first_name', 'last_name', 'username', 'email', 'password')


class OrganizationsSerializer(ModelSerializer):
    departments_count = serializers.SerializerMethodField()
    total_employees_count = serializers.SerializerMethodField()

    class Meta:
        model = Organizations
        fields = '__all__'

    def get_departments_count(self, obj):
        return Departments.objects.filter(organization=obj).count()

    def get_total_employees_count(self, obj):
        return Employees.objects.filter(department__organization=obj).count()


class DepartmentsGetSerializer(ModelSerializer):
    organization = OrganizationsSerializer()
    total_count = serializers.SerializerMethodField()
    total_employees_count = serializers.SerializerMethodField()

    class Meta:
        model = Departments
        fields = '__all__'

    def get_total_count(self, obj):
        return Departments.objects.filter().count()

    def get_total_employees_count(self, obj):
        return Employees.objects.filter(department=obj).count()


class DepatmentsPostPutPatchSerializer(ModelSerializer):
    class Meta:
        model = Departments
        fields = ('name', 'organization')


class EmployeesGetSerializer(ModelSerializer):
    user = CustomUserGetSerializer()
    department = DepartmentsGetSerializer()

    class Meta:
        model = Employees
        fields = '__all__'


class EmployeesPostPutPatchSerializer(ModelSerializer):
    class Meta:
        model = Employees
        fields = ('user', 'status', 'department')

