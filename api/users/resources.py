from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from .serializers import CustomUserPostSerializer
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
            settings.EMAIL_HOST_USER,
            [user.email, ],
            fail_silently=False
        )
        print(f"Result - {res} User email - {user.email} Token - {token.key}")
        return Response({
            'token': token.key,
            'message': 'token has sent on email too'
        })
