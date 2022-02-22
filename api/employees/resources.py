from employees.models import Organizations, Employees, Departments
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .serializers import EmployeesGetSerializer, \
    EmployeesPostPutPatchSerializer, DepartmentsGetSerializer, DepatmentsPostPutPatchSerializer, \
    OrganizationsSerializer
from .permissions import IsAdminOrReadOnly


class EmployeesModelViewSet(ModelViewSet):
    queryset = Employees.objects.all()
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.request.method != 'GET':
            return EmployeesPostPutPatchSerializer
        else:
            return EmployeesGetSerializer

    def perform_update(self, serializer):
        old_status = serializer.instance.status
        new_status = serializer.validated_data['status']
        dep = serializer.instance.department
        if Employees.objects.filter(status=old_status, department=dep).exists():
            Employees.objects.filter(status=old_status, department=dep).update(status=new_status)
            serializer.save()
        serializer.save()


class DepartmentsModelViewSet(ModelViewSet):
    queryset = Departments.objects.all()
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.request.method != 'GET':
            return DepatmentsPostPutPatchSerializer
        else:
            return DepartmentsGetSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        name = self.request.GET.get('name')
        if name:
            return qs.filter(name__icontains=name)
        return qs.all().order_by('name')


class OrganizationsModelViewSet(ModelViewSet):
    queryset = Organizations.objects.all()
    serializer_class = OrganizationsSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        name = self.request.GET.get('name')
        if name:
            return qs.filter(name__icontains=name)
        return qs.all().order_by('-name')