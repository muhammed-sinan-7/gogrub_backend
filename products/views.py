from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from rest_framework import filters, generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import Cart, CartItem

from .models import Category, Product
from .serializers import ProductSerializer

# Create your views here.


class ProductPagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = "page_size"
    max_page_size = 50


class ProductListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        products = Product.objects.all()

        is_special = request.query_params.get("is_special")
        if is_special == "true":
            products = products.filter(is_special=True)

        category = request.query_params.get("category")
        if category:
            products = products.filter(category__name=category)

        paginator = ProductPagination()
        paginated_products = paginator.paginate_queryset(products, request)

        serializer = ProductSerializer(paginated_products, many=True)
        return paginator.get_paginated_response(serializer.data)


class HomePageProductAPIView(APIView):
    def get(self, request):

        special_serializer = ProductSerializer(
            Product.objects.filter(is_special=True).select_related("category")[:12],
            many=True,
        )
        chinese_serializer = ProductSerializer(
            Product.objects.filter(category__name="Chinese")[:10], many=True
        )
        offer_serializer = ProductSerializer(
            Product.objects.filter(category__name="Offer")[:10], many=True
        )

        data = {
            "special_products": special_serializer.data,
            "chinese_products": chinese_serializer.data,
            "offer_products": offer_serializer.data,
        }
        print(data)
        return Response(data, status=status.HTTP_200_OK)


class ProductDetailAPIView(APIView):
    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductSearchAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "category__name", "description"]


class ClearCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        cart_items = CartItem.objects.filter(user=user)

        if cart_items.exists():
            cart_items.delete()
            return Response(
                {"message": "Checkout Successfull", "cart": {"items": []}},
                status=status.HTTP_200_OK,
            )
        return Response("Cart is already empty", status=status.HTTP_400_BAD_REQUEST)
