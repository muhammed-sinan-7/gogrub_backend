from django.db.models import Q
# from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import Product,Category
from users.serializers import USerSerializer
from rest_framework.parsers import FormParser,MultiPartParser,JSONParser
from .serializers import *

# from
# Create your views here.


class CategoryListAPIView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductListCreateAPIView(APIView):
    # Ensure multipart/form-data and files are parsed into request.FILES
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    permission_classes = [IsAdminUser]

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        print("🔥 PRODUCT CREATE HIT")
        print("CONTENT TYPE:", request.content_type)
        serializer = ProductCreateUpdateSerialzier(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            product = serializer.save()
            return Response(
                ProductListSerializer(product).data, status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetailAPIView(APIView):
    def get(self, request, id):
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response(
                {"detail": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProductCreateUpdateSerialzier(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        product = Product.objects.get(id=id)
        serializer = ProductCreateUpdateSerialzier(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ProductDeleteAPIView(APIView):
    def delete(self, request, id):
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response(
                {"detail": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )

        product.delete()
        return Response(
            {"detail": "Product deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )

    #  ------------------- Users ----------------


class UserListAPIView(APIView):
    def get(self, request):
        query = request.query_params.get("search", None)
        users = CustomUser.objects.all()

        if query:
            # Filters users where name OR email contains the search string
            users = users.filter(
                Q(fullname__icontains=query) | Q(email__icontains=query)
            )

        serializer = USerSerializer(users, many=True)
        return Response(serializer.data)


class UserBlockAPIView(APIView):
    def put(self, request, id):
        try:
            user = CustomUser.objects.get(id=id)
            # Toggle the status (If active, make inactive. If inactive, make active)
            user.is_active = not user.is_active
            user.save()

            # Return the updated status so the frontend can sync
            return Response(
                {
                    "id": user.id,
                    "is_active": user.is_active,
                    "message": "User status updated successfully",
                },
                status=status.HTTP_200_OK,
            )
        except CustomUser.DoesNotExist:
            return Response("User Not Exist", status=status.HTTP_404_NOT_FOUND)

    # order ----------------------------------------------


class AdminOrderListAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        orders = Order.objects.select_related("user").prefetch_related("items")
        serializer = AdminOrderSerializer(orders, many=True)
        return Response(serializer.data)


# views.py
class OrderStatusUpdateAPIView(APIView):
    def patch(self, request, pk):
        try:
            # CHANGE: Fetch 'Order' instead of 'OrderItem'
            order = Order.objects.get(id=pk)

            new_status = request.data.get("status")

            # Use the choices defined in your Order model
            valid_statuses = [choice[0] for choice in Order.ORDER_CHOICES]

            if new_status in valid_statuses:
                order.order_status = new_status
                order.save()
                return Response(
                    {"id": str(order.id), "order_status": order.order_status},
                    status=status.HTTP_200_OK,
                )

            return Response(
                {"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Order.DoesNotExist:  # CHANGE: Catch Order.DoesNotExist
            return Response(
                {"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND
            )
