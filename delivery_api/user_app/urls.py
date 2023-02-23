from django.urls import path, include
from .views import (
    UserRegistrationAPIView, UserLoginAPIView, UserLogoutAPIView, UserAddressAPIViewSet,
)
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter

app_name = "users"

router = DefaultRouter(trailing_slash=False)
router.register(r'addresses', UserAddressAPIViewSet, basename='addresses')

urlpatterns = [
    path('', include(router.urls)),

    # Авторизация
    path('register/', UserRegistrationAPIView.as_view()),
    path('login/', UserLoginAPIView.as_view()),
    path('logout/', UserLogoutAPIView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]
