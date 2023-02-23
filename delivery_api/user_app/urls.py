from django.urls import path
from .views import UserRegistrationAPIView, UserLoginAPIView, UserLogoutAPIView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view()),
    path('login/', UserLoginAPIView.as_view()),
    path('logout/', UserLogoutAPIView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view())
]
