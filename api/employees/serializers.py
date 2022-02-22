from rest_framework import serializers
from employees.models import Employees, Organizations, Departments
from rest_framework.serializers import ModelSerializer
from api.users.serializers import CustomUserGetSerializer


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