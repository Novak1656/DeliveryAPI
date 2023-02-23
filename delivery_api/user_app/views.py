from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import UserAddresses

from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, UserSerializer, UserAddressCUDSerializer, UserAddressSerializer,
    UserResetPasswordSerializer
)
from rest_framework_simplejwt.tokens import RefreshToken


class UserRegistrationAPIView(GenericAPIView):
    """
        Endpoint для регистрации пользователя
    """
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer
    http_method_names = ('post',)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = RefreshToken.for_user(user=user)
        resp_data = serializer.data
        resp_data['tokens'] = {'refresh': str(token), 'access': str(token.access_token)}
        return Response(data=resp_data, status=201)


class UserLoginAPIView(GenericAPIView):
    """
        Endpoint для авторизации пользователя
    """
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer
    http_method_names = ('post',)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        serializer = UserSerializer(user)
        resp_data = serializer.data
        token = RefreshToken.for_user(user=user)
        resp_data['tokens'] = {'refresh': str(token), 'access': str(token.access_token)}
        return Response(data=resp_data, status=200)


class UserLogoutAPIView(APIView):
    """
        Endpoint для выхода из аккаунта пользователя
    """
    permission_classes = (IsAuthenticated,)
    http_method_names = ('post',)

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(token=refresh_token)
            token.blacklist()
            return Response(status=205)
        except Exception as error:
            print(f'Error while user logout: {error}')
            return Response(status=400)


class UserAddressAPIViewSet(ModelViewSet):
    """
        Endpoint для адресов пользователя
    """
    permission_classes = (IsAuthenticated,)
    lookup_url_kwarg = 'address_id'

    def get_queryset(self):
        user_id = self.request.user.pk
        if address_id := self.kwargs.get('address_id'):
            return UserAddresses.objects.filter(user_id=user_id, pk=address_id)
        return UserAddresses.objects.filter(user_id=user_id)

    def get_serializer_class(self):
        cur_action = self.action
        if cur_action in ('create', 'update', 'partial_update', 'destroy'):
            return UserAddressCUDSerializer
        return UserAddressSerializer


class UserResetPasswordAPIView(UpdateAPIView):
    """
        Endpoint для смены пароля пользователя
    """
    serializer_class = UserResetPasswordSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ('put',)

    def put(self, request, *args, **kwargs):
        user = request.user
        req_data = request.data
        serializer = self.get_serializer(data=req_data)
        serializer.is_valid(raise_exception=True)
        new_password = serializer.validated_data.get('password1')
        with transaction.atomic():
            user.set_password(new_password)
            user.save()
        return Response(status=200)
