import razorpay
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from cart.models import Cart
from products.models import Product

from .models import Order, OrderItem

razorpay_client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)


class CheckoutPreviewAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        mode = request.query_params.get("mode", "cart")
        items = []
        total = 0

        if mode == "buy_now":
            product_id = request.query_params.get("product_id")
            quantity = int(request.query_params.get("quantity", 1))

            product = Product.objects.get(id=product_id)
            subtotal = product.price * quantity
            total = subtotal

            items.append(
                {
                    "id": product.id,
                    "name": product.name,
                    "image": product.image if product.image else "",
                    "price": float(product.price),
                    "quantity": quantity,
                    "subtotal": float(subtotal),
                }
            )

        else:
            cart = Cart.objects.get(user=request.user)
            for item in cart.items.select_related("product"):
                subtotal = item.price * item.quantity
                total += subtotal

                items.append(
                    {
                        "id": item.product.id,
                        "name": item.product.name,
                        "image": item.product.image if item.product.image else "",
                        "price": float(item.price),
                        "quantity": item.quantity,
                        "subtotal": float(subtotal),
                    }
                )

        return Response(
            {
                "items": items,
                "total": float(total),
                "currency": "INR",
            },
            status=status.HTTP_200_OK,
        )


class CreateOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            with transaction.atomic():  # 🔥 START ATOMIC BLOCK

                mode = request.data.get("mode")
                payment_method = request.data.get("payment_method")
                address = request.data.get("address")

                items = []
                total = 0

                if mode == "buy_now":
                    product = Product.objects.get(id=request.data["product_id"])
                    qty = int(request.data["quantity"])
                    subtotal = product.price * qty
                    total = subtotal
                    items.append((product, qty, subtotal))
                else:
                    cart = Cart.objects.get(user=request.user)
                    for item in cart.items.select_related("product"):
                        subtotal = item.price * item.quantity
                        total += subtotal
                        items.append((item.product, item.quantity, subtotal))

                # 🔥 Create Order
                order = Order.objects.create(
                    user=request.user,
                    total_amount=total,
                    payment_method=payment_method,
                    full_name=address["fullName"],
                    phone=address["phone"],
                    street=address["street"],
                    city=address["city"],
                    zip_code=address["zip"],
                )

                # 🔥 Create OrderItems
                for product, qty, subtotal in items:
                    OrderItem.objects.create(
                        order=order,
                        product_id=product.id,
                        product_name=product.name,
                        product_image=product.image,
                        price=product.price,
                        quantity=qty,
                        subtotal=subtotal,
                    )

                # 🔥 COD FLOW
                if payment_method == "cod":
                    order.payment_status = "pending"
                    order.save()

                    if mode == "cart":
                        Cart.objects.get(user=request.user).items.all().delete()

                    return Response(
                        {"order_id": str(order.id), "cod": True, "success": True},
                        status=status.HTTP_200_OK,
                    )

                # 🔥 ONLINE PAYMENT FLOW
                amount_in_paise = int(total * 100)

                razorpay_order = razorpay_client.order.create(
                    {
                        "amount": amount_in_paise,
                        "currency": "INR",
                        "receipt": f"ord_{order.id.hex}",
                        "payment_capture": "1",
                    }
                )

                order.razorpay_order_id = razorpay_order["id"]
                order.save()

                return Response(
                    {
                        "order_id": str(order.id),
                        "razorpay_order_id": razorpay_order["id"],
                        "razorpay_key": settings.RAZORPAY_KEY_ID,
                        "amount": amount_in_paise,
                        "currency": "INR",
                        "name": "Your Store Name",
                        "description": f"Order #{order.id}",
                        "prefill": {
                            "name": address["fullName"],
                            "contact": address["phone"],
                        },
                    },
                    status=status.HTTP_200_OK,
                )

        except Exception as e:
            # 🔥 NOTHING IS SAVED IF ANY ERROR OCCURS
            return Response(
                {"error": "Order creation failed", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )



@method_decorator(csrf_exempt, name="dispatch")
class VerifyRazorpayPaymentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order_id = request.data.get("order_id")
        razorpay_payment_id = request.data.get("razorpay_payment_id")
        razorpay_order_id = request.data.get("razorpay_order_id")
        razorpay_signature = request.data.get("razorpay_signature")

        try:
            order = Order.objects.get(id=order_id, user=request.user)

            # Verify payment signature
            params_dict = {
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_signature": razorpay_signature,
            }

            razorpay_client.utility.verify_payment_signature(params_dict)

            order.payment_status = "paid"
            order.razorpay_payment_id = razorpay_payment_id
            order.razorpay_signature = razorpay_signature
            order.save()

            mode = request.data.get("mode", "cart")
            if mode == "cart":
                Cart.objects.filter(user=request.user).first().items.all().delete()

            return Response(
                {"success": True, "message": "Payment verified successfully"},
                sttaus=status.HTTP_200_OK,
            )

        except razorpay.errors.SignatureVerificationError:
            order.payment_status = "cancelled"
            order.save()
            return Response(
                {"success": False, "message": "Payment verification failed"}, status=400
            )
        except Exception as e:
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
