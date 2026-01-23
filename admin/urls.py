from django.urls import path
from .views import *

urlpatterns = [
    path('categories/',CategoryListAPIView.as_view()),
    path('products/',ProductListCreateAPIView.as_view()),
    path("products/<int:id>/", ProductDetailAPIView.as_view()),
    path("products/delete/<int:id>/", ProductDeleteAPIView.as_view()),
    path('users/',UserListAPIView.as_view()),
    path('users/block/<int:id>/',UserBlockAPIView.as_view()),
    path('orders/',AdminOrderListAPIView.as_view()),
    path('orders/<uuid:pk>/update-status/',OrderStatusUpdateAPIView.as_view()),
]
