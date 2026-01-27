from django.urls import path

from .views import (
    ClearCartAPIView,
    HomePageProductAPIView,
    ProductDetailAPIView,
    ProductListAPIView,
    ProductSearchAPIView,
)

urlpatterns = [
    path("", ProductListAPIView.as_view()),
    path("homepageproducts/", HomePageProductAPIView.as_view()),
    path("search/", ProductSearchAPIView.as_view()),
    path("<int:id>/", ProductDetailAPIView.as_view()),
    # path('<int:id>/', ProductDetailAPIView.as_view()),
    path("clear/", ClearCartAPIView.as_view()),
]
