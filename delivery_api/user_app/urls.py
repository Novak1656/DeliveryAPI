from django.urls import path, include
from .views import (
    UserRegistrationAPIView, UserLoginAPIView, UserLogoutAPIView, UserAddressAPIViewSet, UserResetPasswordAPIView,
    UserDeleteAPIView, UserUpdateAPIView
)
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter

app_name = "users"

router = DefaultRouter(trailing_slash=False)
router.register(r'addresses', UserAddressAPIViewSet, basename='addresses')

urlpatterns = [
    path('', include(router.urls)),

    # Авторизация
    path('register', UserRegistrationAPIView.as_view(), name='register'),
    path('login', UserLoginAPIView.as_view(), name='login'),
    path('logout', UserLogoutAPIView.as_view(), name='logout'),
    path('token/refresh', TokenRefreshView.as_view(), name='refresh_token'),

    # Редактирование пользовательских данных
    path('reset_password', UserResetPasswordAPIView.as_view(), name='reset_password'),
    path('delete', UserDeleteAPIView.as_view(), name='delete_user'),
    path('update', UserUpdateAPIView.as_view(), name='update_user'),
]
