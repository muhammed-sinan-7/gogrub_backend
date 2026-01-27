from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import Product

from .models import Cart, CartItem
from .serializers import CartItemSerializer, CartSerializer

# Create your views here.


class CartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.items.select_related("product").all()

        serializer = CartItemSerializer(cart_items, many=True)

        return Response(
            {
                "cart": {
                    "id": str(cart.cart_id),
                    "total_items": cart.get_item_count(),
                    "total_price": float(cart.get_total()),
                    "items": serializer.data,
                }
            }
        )

    def post(self, request):
        user = request.user
        cart = Cart.objects.get(user=user)

        product = Product.objects.get(id=request.data["product_id"])
        quantity = request.data.get("quantity", 1)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={"quantity": quantity, "price": product.price},
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)


class CartDeleteAPIView(APIView):
    def delete(self, request):
        user = request.user
        cart = Cart.objects.get(user=user)
        cart_item_id = request.data.get("cart_item_id")

        cart_item = CartItem.objects.filter(cart=cart, id=cart_item_id).first()
        cart_item.delete()
        return Response("Deleted Succesfully")


class UpdateQuantityAPIView(APIView):
    def put(self, request):
        user = request.user
        cart = Cart.objects.get(user=user)
        cart_item_id = request.data.get("cart_item_id")
        quantity = request.data.get("quantity")
        try:

            cart_item = CartItem.objects.get(cart=cart, id=cart_item_id)
        except CartItem.DoesNotExist:
            return Response(
                {"error": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND
            )

        cart_item.quantity = quantity
        cart_item.save()
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)
