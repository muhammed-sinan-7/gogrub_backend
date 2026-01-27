from django.urls import path

from .views import DeleteWishlistAPIView, WishlistAPIView

urlpatterns = [
    path("", WishlistAPIView.as_view()),
    path("delete/", DeleteWishlistAPIView.as_view()),
]
