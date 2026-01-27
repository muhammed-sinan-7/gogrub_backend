# from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import Product

from .models import Wishlist, WishlistItem
from .serializers import WishlistItemSerializer

# Create your views here.


class WishlistAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # user = request.user

        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
        products = wishlist.items.select_related("product").all()
        print(products)

        serializer = WishlistItemSerializer(products, many=True)

        return Response(serializer.data)

    def post(self, request):
        user = request.user
        wishlist, _ = Wishlist.objects.get_or_create(user=user)

        product_id = request.data.get("product_id")

        exist = WishlistItem.objects.filter(
            wishlist=wishlist, product_id=product_id
        ).exists()

        if exist:
            return Response(
                {"message": "Product Already added"}, status=status.HTTP_400_BAD_REQUEST
            )

        product = Product.objects.get(id=product_id)
        wishlist_item = WishlistItem.objects.create(wishlist=wishlist, product=product)

        serializer = WishlistItemSerializer(wishlist_item)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteWishlistAPIView(APIView):
    def delete(self, request):
        user = request.user
        try:

            wishlist = WishlistItem.objects.get(
                wishlist__user=user, id=request.data.get("item_id")
            )

        except WishlistItem.DoesNotExist:
            return Response(
                {"error": "Wishlist item not found"}, status=status.HTTP_404_NOT_FOUND
            )

        wishlist.delete()
        return Response(
            {"message": "Item removed from wishlist"}, status=status.HTTP_204_NO_CONTENT
        )
