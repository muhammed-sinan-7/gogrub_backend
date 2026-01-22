from django.urls import path
from .views import( ProductListAPIView,
                   HomePageProductAPIView,
                    ProductDetailAPIView,
                    ProductSearchAPIView,
                    ClearCartAPIView
                   )

urlpatterns = [
    path('', ProductListAPIView.as_view()),
    path('homepageproducts/', HomePageProductAPIView.as_view()),
    path('search/', ProductSearchAPIView.as_view()),
    path('<int:id>/', ProductDetailAPIView.as_view()),
    # path('<int:id>/', ProductDetailAPIView.as_view()),
    path('clear/',ClearCartAPIView.as_view())
]
