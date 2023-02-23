from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer
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
