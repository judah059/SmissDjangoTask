from django.conf import settings
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from taskapp.models import CustomUser, Organizations, Employees, Departments
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from taskapp.API.serializers import CustomUserGetSerializer, CustomUserPostSerializer, EmployeesGetSerializer, EmployeesPostPutPatchSerializer, DepartmentsGetSerializer, DepatmentsPostPutPatchSerializer, \
    OrganizationsSerializer
from taskapp.API.permissions import IsAdminOrReadOnly
from rest_framework import permissions
from django.core.mail import send_mail
from django.conf import settings

UserModel = get_user_model()


class ApiRegistration(CreateAPIView):
    model = UserModel
    permission_classes = [permissions.AllowAny]
    serializer_class = CustomUserPostSerializer


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        res = send_mail(
            'Token',
            token.key,
            settings.DEFAULT_FROM_EMAIL,
            [user.email,],
            fail_silently=False
        )
        print(f"Result - {res} User email - {user.email} Token - {token.key}")
        return Response({
            'token': token.key,
            'message': 'token has sent on email too'
        })


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


class OrganizationsModelViewSet(ModelViewSet):
    queryset = Organizations.objects.all()
    serializer_class = OrganizationsSerializer
    permission_classes = [IsAdminOrReadOnly]
