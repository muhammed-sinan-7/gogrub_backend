# from drf_yasg import openapi
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Sum
from django.shortcuts import render
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from drf_yasg.utils import swagger_auto_schema
from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponse
from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer

from .models import CustomUser
from .serializers import LoginSerializer, RegisterSerializer, USerSerializer


class PasswordResetRequestView(APIView):
    def post(self, request):
        email = request.data.get("email")
        user = CustomUser.objects.filter(email=email).first()

        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = f"http://localhost:5173/password-reset-confirm/{uid}/{token}"

            send_mail(
                "GoGrub - Password Reset",
                f"Click the link to reset your password: {reset_link}",
                "gogrub7@gmail.com",
                [email],
                fail_silently=False,
            )
        return Response(
            {"detail": "If an account exists with this email, a link has been sent."},
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmView(APIView):
    def post(self, request):
        uidb64 = request.data.get("uid")
        token = request.data.get("token")
        new_password = request.data.get("new_password")

        if not new_password:
            return Response(
                {"detail": "Password is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            return Response(
                {"detail": "Invalid reset link."}, status=status.HTTP_400_BAD_REQUEST
            )

        if not default_token_generator.check_token(user, token):
            return Response(
                {"detail": "Reset link has expired or is invalid."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(new_password)
        user.save()

        return Response(
            {"detail": "Password reset successful."}, status=status.HTTP_200_OK
        )


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User Created Successfully"}, status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    serializer_class = LoginSerializer

    @swagger_auto_schema(
        request_body=LoginSerializer, responses={200: "Login successful"}
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "fullname": user.fullname,
                    "is_staff": user.is_staff,
                },
            },
        )


# class LogoutAPIView(APIView):


class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            orders = Order.objects.filter(user=user)

            total_spent = (
                orders.filter(payment_status="paid")
                .aggregate(total_spent=Sum("price"))
                .get("total_spent", 0)
                or 0
            )

            order_data = OrderSerializer(orders, many=True).data

            return Response(
                {
                    "user": {
                        "id": user.id,
                        "fullname": getattr(user, "fullname", None),
                        "email": user.email,
                    },
                    "orders": order_data,
                    "stats": {
                        "total_orders": orders.count(),
                        "total_spent": float(total_spent),
                    },
                    "last_address": orders.first().street if orders.exists() else None,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"detail": "Failed to load profile"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class GoogleLoginAPIView(APIView):
    def post(self, request):
        token = request.data.get("id_token")

        if not token:
            return Response({"detail": "Token missing"}, status=400)

        try:
            idinfo = id_token.verify_oauth2_token(
                token, requests.Request(), settings.GOOGLE_CLIENT_ID
            )

            email = idinfo.get("email")
            name = idinfo.get("name", "")

            user, created = CustomUser.objects.get_or_create(
                email=email, defaults={"username": email, "first_name": name}
            )

            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "is_staff": user.is_staff,
                    },
                }
            )

        except ValueError:
            return Response(
                {"detail": "Invalid Google token"}, status=status.HTTP_401_UNAUTHORIZED
            )







def health(request):
    return JsonResponse({"status": "ok"})
