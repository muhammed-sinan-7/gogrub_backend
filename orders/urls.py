from django.urls import path

from .views import (
    CheckoutPreviewAPIView,
    CreateOrderAPIView,
    VerifyRazorpayPaymentAPIView,
)

urlpatterns = [
    path(
        "checkout/preview/", CheckoutPreviewAPIView.as_view(), name="checkout-preview"
    ),
    path("create/", CreateOrderAPIView.as_view(), name="create-order"),
    path(
        "verify-payment/", VerifyRazorpayPaymentAPIView.as_view(), name="verify-payment"
    ),
]
