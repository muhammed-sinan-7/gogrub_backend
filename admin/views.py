from django.shortcuts import render
from products.models import Product
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import *
from django.db.models import Q
from users.serializers import USerSerializer
from rest_framework.permissions import IsAdminUser,IsAuthenticated
# from 
# Create your views here.

class CategoryListAPIView(APIView):
    def get(self,request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        print(serializer.data)
        return Response(serializer.data,status=status.HTTP_200_OK)


class ProductListCreateAPIView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        # The 'context' ensures the serializer has access to the request for images/user
        serializer = ProductCreateUpdateSerialzier(
            data=request.data,
            context={"request": request}
        )

        if serializer.is_valid():
            # Automatically assign the logged-in admin to the product
            product = serializer.save()
            return Response(
                ProductListSerializer(product).data,
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetailAPIView(APIView):
    def get(self, request, id):
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response(
                {"detail": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProductCreateUpdateSerialzier(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, id):
        product = Product.objects.get(id=id)
        serializer = ProductCreateUpdateSerialzier(
            product, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    
class ProductDeleteAPIView(APIView):
    def delete(self, request, id):
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response(
                {"detail": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        product.delete()
        return Response(
            {"detail": "Product deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
    
    
    
    
    #  ------------------- Users ----------------
    
class UserListAPIView(APIView):
    def get(self, request):
        query = request.query_params.get('search', None)
        users = CustomUser.objects.all()

        if query:
            # Filters users where name OR email contains the search string
            users = users.filter(
                Q(fullname__icontains=query) | 
                Q(email__icontains=query)
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
            return Response({
                "id": user.id,
                "is_active": user.is_active,
                "message": "User status updated successfully"
            }, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response("User Not Exist", status=status.HTTP_404_NOT_FOUND)
    
    
    # order ---------------------------------------------- 
    
    
    
class OrderListAPIView(APIView):
    def get(self, request):
        # Use double underscores to traverse relationships
        orders = OrderItem.objects.select_related('order__user').all()
        serializer = OrderItemListSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

# views.py
class OrderStatusUpdateAPIView(APIView):
    def patch(self, request, pk):
        try:
            # We fetch the OrderItem using the ID from React
            order_item = OrderItem.objects.get(id=pk)
            order = order_item.order  # Get the parent Order
            
            new_status = request.data.get('status')
            
            # Check if the status is valid based on Order model choices
            if new_status in dict(Order.ORDER_CHOICES):
                order.order_status = new_status
                order.save()
                return Response({
                    "id": pk, 
                    "order_status": new_status
                }, status=status.HTTP_200_OK)
                
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)
        except OrderItem.DoesNotExist:
            return Response({"error": "OrderItem not found"}, status=status.HTTP_404_NOT_FOUND)
        
        