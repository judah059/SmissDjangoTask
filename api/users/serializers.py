from rest_framework import serializers
from users.models import CustomUser
from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class CustomUserGetSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', )


class CustomUserPostSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = UserModel.objects.create_user(username=validated_data['username'], email=validated_data['email'],
                                             password=validated_data['password'])
        return user

    class Meta:
        model = UserModel
        fields = ('first_name', 'last_name', 'username', 'email', 'password')
