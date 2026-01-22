from django.urls import path
from .views import (
    RegisterAPIView,
    LoginAPIView,
    ProfileAPIView,
    PasswordResetConfirmView,
    PasswordResetRequestView,
    GoogleLoginAPIView
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", RegisterAPIView.as_view()),
    path("login/", LoginAPIView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
    path("me/", ProfileAPIView.as_view()),
    path("password_reset/", PasswordResetRequestView.as_view()),
    path("password_reset_confirm/", PasswordResetConfirmView.as_view()),
    path("google/", GoogleLoginAPIView.as_view()),
]
