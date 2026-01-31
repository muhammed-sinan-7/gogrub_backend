from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    GoogleLoginAPIView,
    LoginAPIView,
    PasswordResetConfirmView,
    PasswordResetRequestView,
    ProfileAPIView,
    RegisterAPIView,
    version
)

urlpatterns = [
    path("register/", RegisterAPIView.as_view()),
    path("login/", LoginAPIView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
    path("me/", ProfileAPIView.as_view()),
    path("password_reset/", PasswordResetRequestView.as_view()),
    path("password_reset_confirm/", PasswordResetConfirmView.as_view()),
    path("google/", GoogleLoginAPIView.as_view()),
    path('version/',version)
]
