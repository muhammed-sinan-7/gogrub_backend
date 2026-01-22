from django.urls import path
from .views import CartAPIView,CartDeleteAPIView,UpdateQuantityAPIView

urlpatterns = [
    path('',CartAPIView.as_view()),
    path('delete/',CartDeleteAPIView.as_view()),
    path('quantity/',UpdateQuantityAPIView.as_view()),
]

