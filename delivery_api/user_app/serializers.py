from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework import serializers
from .models import User, UserAddresses


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


class UserAddressCUDSerializer(serializers.ModelSerializer):
    """
        Сериализатор для создания, обновления и удаления адреса пользователя
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserAddresses
        fields = ('id', 'user', 'city', 'street', 'house', 'entrance', 'floor', 'flat',)


class UserAddressSerializer(serializers.ModelSerializer):
    """
        Сериализатор для адресов пользователя
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserAddresses
        exclude = ('last_order',)


class UserResetPasswordSerializer(serializers.Serializer):
    """
        Сериализатор для смены пароля пользователя
    """
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        password1 = data.get('password1')
        password2 = data.get('password2')
        if password1 != password2:
            raise serializers.ValidationError('Пароли не совпадают')
        return data
