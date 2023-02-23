from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
        Сериализатор пользователя
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'birthday')


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
        Сериализатор для регистрации пользователя
    """
    created_at = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name', 'birthday', 'created_at')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.Serializer):
    """
        Сериализатор для авторизации пользователя
    """
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Неверный логин или пароль')