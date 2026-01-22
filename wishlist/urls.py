from django.urls import path
from .views import WishlistAPIView,DeleteWishlistAPIView

urlpatterns = [
    path('',WishlistAPIView.as_view()),
    path('delete/',DeleteWishlistAPIView.as_view()),
]
